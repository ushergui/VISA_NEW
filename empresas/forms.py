from django import forms
from .models import Contabilidade, Cnae, Empresas, Risco, Legislacao, ProtocoloEmpresa, Inspecao, AcaoProdutividade, Produtividade
from cadastros.models import Logradouro, Fiscal, Cidade, Bairro
from django.core.exceptions import ValidationError
import re


class ContabilidadeForm(forms.ModelForm):
    class Meta:
        model = Contabilidade
        fields = '__all__'

class CnaeForm(forms.ModelForm):
    class Meta:
        model = Cnae
        fields = '__all__'

def valida_cpf(cpf):
    # remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)

    # verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # cálculo de validação de CPF
    total = 0
    peso = 10

    for i in range(9):
        total += int(cpf[i]) * peso
        peso -= 1

    digito = 11 - total % 11

    if digito > 9:
        digito1 = 0
    else:
        digito1 = digito

    total = 0
    peso = 11

    for i in range(10):
        total += int(cpf[i]) * peso
        peso -= 1

    digito = 11 - total % 11

    if digito > 9:
        digito2 = 0
    else:
        digito2 = digito

    return cpf[-2:] == f'{digito1}{digito2}'


def valida_cnpj(cnpj):
    # remove caracteres não numéricos
    cnpj = re.sub(r'\D', '', cnpj)

    # verifica se o CNPJ tem 14 dígitos
    if len(cnpj) != 14:
        return False

    # cálculo de validação de CNPJ
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    temp_cnpj = cnpj[:-2]

    total = sum([int(a)*b for a, b in zip(temp_cnpj, pesos)])

    digito = 11 - total % 11

    if digito > 9:
        digito1 = 0
    else:
        digito1 = digito

    # inserir o primeiro dígito verificador
    temp_cnpj += str(digito1)

    # sequência de pesos a ser usada no segundo cálculo
    pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    total = sum([int(a)*b for a, b in zip(temp_cnpj, pesos)])

    digito = 11 - total % 11

    if digito > 9:
        digito2 = 0
    else:
        digito2 = digito

    return cnpj[-2:] == f'{digito1}{digito2}'

class LogradouroModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.tipo} {obj.nome_logradouro} - {obj.bairro.nome_bairro}"


class EmpresasForm(forms.ModelForm):
    logradouro_empresa = LogradouroModelChoiceField(queryset=Logradouro.objects.select_related('bairro', 'bairro__cidade').all())
    risco_empresa = forms.ModelChoiceField(queryset=Risco.objects.all())
    cnae = forms.ModelMultipleChoiceField(
        queryset=Cnae.objects.select_related('risco_cnae').all(),
        widget=forms.SelectMultiple(attrs={'class': 'cnae'}), # Adicione esta linha
    )
    contabilidade = forms.ModelChoiceField(queryset=Contabilidade.objects.all())

    class Meta:
        model = Empresas
        fields = '__all__'
        widgets = {
            'risco_empresa': forms.Select(attrs={'id': 'id_risco_empresa'}),
        }
    def __init__(self, *args, **kwargs):
        super(EmpresasForm, self).__init__(*args, **kwargs)
        cidade_ss_paraiso = Cidade.objects.filter(nome_cidade="SAO SEBASTIAO DO PARAISO").first()
        
        if cidade_ss_paraiso:
            bairros_ss_paraiso = Bairro.objects.filter(cidade=cidade_ss_paraiso)
            logradouros_ss_paraiso = Logradouro.objects.filter(bairro__in=bairros_ss_paraiso)
            self.fields['logradouro_empresa'].queryset = logradouros_ss_paraiso
        else:
            self.fields['logradouro_empresa'].queryset = Logradouro.objects.none()

    def clean_cpf_responsavel_legal(self):
        cpf = self.cleaned_data.get('cpf_responsavel_legal')
        if cpf and not valida_cpf(cpf):
            raise ValidationError("CPF inválido!")
        return cpf

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj and not valida_cnpj(cnpj):
            raise ValidationError("CNPJ inválido!")
        return cnpj


class EmpresasObservacoesForm(forms.ModelForm):
    observacoes = forms.CharField(widget=forms.Textarea, required=False)  # Aqui está a mudança

    class Meta:
        model = Empresas
        fields = ['observacoes']

class RiscoForm(forms.ModelForm):
    class Meta:
        model = Risco
        fields = ['risco', 'valor_risco']


class LegislacaoForm(forms.ModelForm):
    class Meta:
        model = Legislacao
        fields = '__all__'

class ProtocoloEmpresaForm(forms.ModelForm):
    class Meta:
        model = ProtocoloEmpresa
        fields = '__all__' 

class InspecaoForm(forms.ModelForm):
    class Meta:
        model = Inspecao
        # remover o protocolo dos fields
        fields = ['data_inspecao', 'vigirisco','data_relatorio', 'legislacao', 'desenvolvimento', 'inadequacoes', 'observacoes', 'conclusao']


class AcaoProdutividadeForm(forms.ModelForm):
    class Meta:
        model = AcaoProdutividade
        fields = ['codigo_produtividade', 'acao', 'pontos']


class ProdutividadeForm(forms.ModelForm):
    class Meta:
        model = Produtividade
        fields = ('data_saida_fiscal', 'tempo_gasto', 'mes_produtividade', 'inspecao', 'fiscal_responsavel', 'fiscal_auxiliar', 'total')  
        widgets = {
            'fiscal_responsavel': forms.Select(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, inspecao=None, **kwargs):
        super().__init__(*args, **kwargs)
        if 'fiscal_responsavel' in self.initial:
            self.fields['fiscal_auxiliar'].queryset = Fiscal.objects.exclude(id=self.initial['fiscal_responsavel'].id)

        # Criando dinamicamente os campos de multiplicador
        for acao in AcaoProdutividade.objects.all():
            self.fields[f'multiplicador_{acao.id}'] = forms.DecimalField(
                decimal_places=1,
                max_digits=3,
                required=False,
            )

    def clean(self):
        cleaned_data = super().clean()
        
        # Verificação para cada multiplicador
        for field in self.fields:
            if 'multiplicador' in field:
                multiplicador = cleaned_data.get(field)

                allowed_values = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5]  # Continue a lista conforme necessário

                if multiplicador is not None and multiplicador not in allowed_values:
                    self.add_error(field, "O valor do multiplicador é inválido.")
        
        inspecao = cleaned_data.get("inspecao")
        
        if inspecao and Produtividade.objects.filter(inspecao=inspecao).exists():
            self.add_error('inspecao', "Produtividade com esta Inspeção já existe.")
        
        return cleaned_data

    
# SE DER PAU EMBAIXO TA PRONTO
'''class ProdutividadeForm(forms.ModelForm):
    class Meta:
        model = Produtividade
        fields = ('protocolo', 'data_saida_fiscal', 'tempo_gasto', 'mes_produtividade', 'inspecao', 'fiscal_responsavel', 'fiscal_auxiliar', 'total')
        widgets = {
    'protocolo': forms.Select(attrs={'disabled': 'disabled'}),
    'fiscal_responsavel': forms.Select(attrs={'disabled': 'disabled'}),
}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'fiscal_responsavel' in self.initial:
            self.fields['fiscal_auxiliar'].queryset = Fiscal.objects.exclude(id=self.initial['fiscal_responsavel'].id)

    def clean(self):
        cleaned_data = super().clean()
        inspecao = cleaned_data.get("inspecao")
        
        if Produtividade.objects.filter(inspecao=inspecao).exists():
            raise forms.ValidationError("Produtividade com esta Inspeção já existe.")
        
        return cleaned_data
        '''

class ProdutividadeFormEdit(forms.ModelForm):
    class Meta:
        model = Produtividade
        fields = ('total', 'data_saida_fiscal', 'tempo_gasto', 'mes_produtividade', 'inspecao', 'fiscal_auxiliar')

    protocolo = forms.CharField(max_length=200, disabled=True, required=False)
    fiscal_responsavel = forms.CharField(max_length=200, disabled=True, required=False)

    def __init__(self, *args, **kwargs):
        protocolo = kwargs.pop('protocolo', None)
        fiscal_responsavel = kwargs.pop('fiscal_responsavel', None)
        super().__init__(*args, **kwargs)

        if protocolo:
            self.fields['protocolo'].initial = protocolo
        if fiscal_responsavel:
            self.fields['fiscal_responsavel'].initial = fiscal_responsavel

        if 'fiscal_responsavel' in self.initial:
            self.fields['fiscal_auxiliar'].queryset = Fiscal.objects.exclude(id=self.initial['fiscal_responsavel'].id)




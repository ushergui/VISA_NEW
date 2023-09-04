from django import forms
from .models import Contabilidade, Cnae, Empresas, Risco, Legislacao, ProtocoloEmpresa, Inspecao, AcaoProdutividade, Produtividade, AcaoProdutividadeRel
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
        widget=forms.SelectMultiple(attrs={'class': 'cnae'}), 
        label='CNAE(s) Secundário(s)',
        required=False,  
    )
    cnae_principal = forms.ModelChoiceField(
        queryset=Cnae.objects.select_related('risco_cnae').all(),
        label='CNAE Principal'  
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
    
    def clean(self):
        cleaned_data = super().clean()
        cnae_principal = cleaned_data.get('cnae_principal')
        cnaes_secundarios = cleaned_data.get('cnae')

        # Checa se o cnae_principal está na lista de cnaes_secundarios
        if cnae_principal and cnaes_secundarios and cnae_principal in cnaes_secundarios:
            raise forms.ValidationError("O CNAE principal não pode ser o mesmo que um dos CNAEs secundários.")

        return cleaned_data


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

#FUNCIONANDO
class ProdutividadeForm(forms.ModelForm):
    class Meta:
        model = Produtividade
        fields = ['protocolo', 'acoes', 'total', 'data_saida_fiscal', 'tempo_gasto', 'mes_produtividade', 'inspecao', 'fiscal_responsavel', 'fiscais_auxiliar', 'validacao']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.inspecao:
            self.fields['inspecao'].initial = self.instance.inspecao
            self.fields['inspecao'].disabled = True
        else:
            self.fields['inspecao'].disabled = True
        # Adicionando campos de multiplicador para cada ação
        for acao in AcaoProdutividade.objects.all():
            self.fields[f'multiplicador-{acao.id}'] = forms.DecimalField(max_digits=3, decimal_places=1, required=False)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'inspecao' in self.cleaned_data:
            try:
                instance.inspecao = Inspecao.objects.get(id=self.cleaned_data['inspecao'])
            except (Inspecao.DoesNotExist, ValueError):
                instance.inspecao = None
        if commit:
            instance.save()
        # Resto do seu código aqui
        return instance

class ProdutividadeFormEdit(forms.ModelForm):
    class Meta:
        model = Produtividade
        fields = ['protocolo', 'acoes', 'total', 'data_saida_fiscal', 'tempo_gasto', 'mes_produtividade', 'inspecao', 'fiscal_responsavel', 'fiscais_auxiliar', 'validacao']

class EmpresaCnaeForm(forms.ModelForm):
    cnae = forms.ModelMultipleChoiceField(
        queryset=Cnae.objects.select_related('risco_cnae').all(),
        widget=forms.SelectMultiple(attrs={'class': 'cnae'}), 
        label='CNAE(s) Secundário(s)',
        required=False,  
    )
    cnae_principal = forms.ModelChoiceField(
        queryset=Cnae.objects.select_related('risco_cnae').all(),
        label='CNAE Principal'  
    )

    class Meta:
        model = Empresas
        fields = ['razao', 'cnae_principal', 'cnae', 'risco_empresa']
    
    def clean(self):
        cleaned_data = super().clean()
        cnae_principal = cleaned_data.get('cnae_principal')
        cnaes_secundarios = cleaned_data.get('cnae')

        # Checa se o cnae_principal está na lista de cnaes_secundarios
        if cnae_principal and cnaes_secundarios and cnae_principal in cnaes_secundarios:
            raise forms.ValidationError("O CNAE principal não pode ser o mesmo que um dos CNAEs secundários.")

        return cleaned_data
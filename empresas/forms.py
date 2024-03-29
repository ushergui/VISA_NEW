from django import forms
from .models import Contabilidade, Cnae, Empresas, Risco, Legislacao, ProtocoloEmpresa, Inspecao, AcaoProdutividade, Produtividade, AcaoProdutividadeRel, PlanejamentoInspecao
from cadastros.models import Logradouro, Fiscal, Cidade, Bairro
from django.core.exceptions import ValidationError
import re
from django.utils.text import capfirst
from django.forms import ModelChoiceField


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
        
class EmpresasInscricaoForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = ['inscricao_estadual']

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
        fields = ['acoes', 'total', 'tempo_gasto', 'mes_produtividade', 'inspecao', 'validacao']
        widgets = {
            'inspecao': forms.HiddenInput(),  # Escondendo o campo inspecao porque você vai amarrá-lo a um ID específico
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Este é o passo crucial
        self.fields['acoes'] = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple, queryset=AcaoProdutividade.objects.all())
        self.fields['fiscal_auxiliar'] = forms.ModelMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple, queryset=Fiscal.objects.all())


class ProdutividadeAcaoForm(forms.ModelForm):
    class Meta:
        model = AcaoProdutividadeRel
        fields = ['acao_produtividade', 'multiplicador']

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
    
def capitalize_name(name):
    articles = ['de', 'e', 'da', 'do', 'das', 'dos', 's/n']
    roman_numerals = ['II', 'III', 'VI', 'VII', 'XIII', 'XXIII', 'IV', 'LTDA', 'S/N']
    words = name.split(' ')
    for i, word in enumerate(words):
        if word.lower() in articles:
            words[i] = word.lower()
        elif word.upper() in roman_numerals:
            words[i] = word.upper()
        else:
            words[i] = capfirst(word.lower())
    return ' '.join(words)

class PlanejamentoInspecaoForm(forms.ModelForm):
    empresa = ModelChoiceField(
        queryset=Empresas.objects.all(),
        label='Empresa',
        empty_label="Selecione a Empresa",
        widget=forms.Select(attrs={'class': 'custom-select'})
    )
    
    def __init__(self, *args, **kwargs):
        super(PlanejamentoInspecaoForm, self).__init__(*args, **kwargs)
        self.fields['empresa'].label_from_instance = self.label_from_instance_empresa

    def clean(self):
        cleaned_data = super().clean()
        empresa = cleaned_data.get("empresa")
        ano = cleaned_data.get("ano")

        # Exclui o planejamento atual da verificação se estiver em modo de edição
        planejamento_atual_id = self.instance.id if self.instance else None

        if PlanejamentoInspecao.objects.exclude(id=planejamento_atual_id).filter(empresa=empresa, ano=ano).exists():
            raise ValidationError("Já existe um planejamento para esta empresa neste ano.")

        return cleaned_data

    def label_from_instance_empresa(self, obj):
        # Aplica a função de capitalização ao nome da empresa.
        empresa_razao = capitalize_name(obj.razao)
        cnae_codigo = obj.cnae_principal.codigo_cnae
        cnae_descricao = obj.cnae_principal.descricao_cnae
        risco_descricao = obj.cnae_principal.risco_cnae.risco
        return f"{empresa_razao} - {cnae_codigo} - {cnae_descricao} - {risco_descricao}"

    class Meta:
        model = PlanejamentoInspecao
        fields = ['fiscal', 'empresa', 'ano', 'inspecao_realizada']
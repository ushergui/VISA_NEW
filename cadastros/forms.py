from django import forms
from .models import Logradouro, Bairro, Proprietario, Logradouro, Protocolo, Terreno, Inspecao, Infracao, FeriadoRecesso
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


class LogradouroForm(forms.ModelForm):
    bairro = forms.ModelChoiceField(
        queryset=Bairro.objects.select_related('cidade__estado').all(),
    )

    class Meta:
        model = Logradouro
        fields = ['tipo', 'nome_logradouro', 'bairro', 'cep']

class LogradouroUpdateForm(forms.ModelForm):
    bairro = forms.ModelChoiceField(queryset=Bairro.objects.select_related('cidade__estado').all())

    class Meta:
        model = Logradouro
        fields = ['tipo', 'nome_logradouro', 'bairro', 'cep']

class ProprietarioForm(forms.ModelForm):
    logradouro_proprietario = forms.ModelChoiceField(queryset=Logradouro.objects.select_related('bairro__cidade__estado').all())

    class Meta:
        model = Proprietario
        fields = ['nome_proprietario', 'logradouro_proprietario', 'numero_proprietario', 'complemento_proprietario']

class ProprietarioUpdateForm(forms.ModelForm):
    logradouro_proprietario = forms.ModelChoiceField(queryset=Logradouro.objects.select_related('bairro__cidade__estado').all())

    class Meta:
        model = Proprietario
        fields = ['nome_proprietario', 'logradouro_proprietario', 'numero_proprietario', 'complemento_proprietario']

class ProtocoloForm(forms.ModelForm):
    logradouro = forms.ModelChoiceField(queryset=Logradouro.objects.select_related('bairro__cidade__estado').all())

    class Meta:
        model = Protocolo
        fields = ['protocolo', 'solicitante_protocolo', 'logradouro', 'descricao_protocolo', 'ouvidoria',
                  'status_protocolo', 'entrada_protocolo']

class ProtocoloUpdateForm(forms.ModelForm):
    logradouro = forms.ModelChoiceField(queryset=Logradouro.objects.select_related('bairro__cidade__estado').all())

    class Meta:
        model = Protocolo
        fields = ['protocolo', 'solicitante_protocolo', 'logradouro', 'descricao_protocolo', 'ouvidoria', 'observacoes',
                  'status_protocolo', 'entrada_protocolo', 'encerramento_protocolo']

class TerrenoForm(forms.ModelForm):
    logradouro_terreno = forms.ModelChoiceField(queryset=Logradouro.objects.select_related('bairro__cidade__estado').all())
    logradouro_correspondencia = forms.ModelChoiceField(queryset=Logradouro.objects.select_related('bairro__cidade__estado').all())

    class Meta:
        model = Terreno
        fields = ['inscricao', 'logradouro_terreno', 'numero_terreno', 'complemento_terreno',
                  'proprietario', 'quadra', 'lote', 'area', 'logradouro_correspondencia',
                  'numero_correspondencia', 'complemento_correspondencia', 'tipo_de_imovel']

class TerrenoUpdateForm(forms.ModelForm):
    logradouro_terreno = forms.ModelChoiceField(queryset=Logradouro.objects.select_related('bairro__cidade__estado').all())
    logradouro_correspondencia = forms.ModelChoiceField(queryset=Logradouro.objects.select_related('bairro__cidade__estado').all())

    class Meta:
        model = Terreno
        fields = ['inscricao', 'logradouro_terreno', 'numero_terreno', 'complemento_terreno',
                  'proprietario', 'lote', 'quadra', 'area', 'logradouro_correspondencia',
                  'numero_correspondencia', 'complemento_correspondencia', 'tipo_de_imovel']

class InspecaoForm(forms.ModelForm):
    protocolo = forms.ModelChoiceField(queryset=Protocolo.objects.select_related('logradouro').all())
    terreno = forms.ModelChoiceField(queryset=Terreno.objects.select_related('logradouro_terreno', 'logradouro_correspondencia').all())

    class Meta:
        model = Inspecao
        fields = ['protocolo', 'terreno', 'foto_inspecao_1', 'data_inspecao1', 'horario_inspecao1', 'data_relatorio1',
                  'fiscal', 'produtidade_inspecao', 'limpo', 'mato', 'entulho', 'lixo', 'carcaca', 'material', 'pneu',
                  'outro', 'movel']

class InspecaoUpdateForm(forms.ModelForm):
    protocolo = forms.ModelChoiceField(queryset=Protocolo.objects.select_related('logradouro').all())
    terreno = forms.ModelChoiceField(queryset=Terreno.objects.select_related('logradouro_terreno', 'logradouro_correspondencia').all())

    class Meta:
        model = Inspecao
        fields = ['protocolo', 'terreno', 'foto_inspecao_1', 'data_inspecao1', 'horario_inspecao1', 'data_relatorio1',
                  'fiscal', 'produtidade_inspecao', 'limpo', 'mato', 'entulho', 'lixo', 'carcaca', 'material', 'pneu',
                  'outro', 'movel']

class InfracaoCreateForm(forms.ModelForm):
    inspecao = forms.ModelChoiceField(queryset=Inspecao.objects.select_related('protocolo', 'terreno').all())

    class Meta:
        model = Infracao
        fields = ['inspecao', 'data_auto', 'produtividade_infracao']

class InfracaoUpdateForm(forms.ModelForm):
    inspecao = forms.ModelChoiceField(queryset=Inspecao.objects.select_related('protocolo', 'terreno').all())

    class Meta:
        model = Infracao
        fields = ['inspecao', 'data_auto', 'rastreio_infracao', 'status_rastreio', 'data_entrega_autuacao', 'prazo_defesa',
                  'nome_recebedor', 'numero_format_ano', 'protocolo_defesa', 'entrada_protocolo', 'quem', 'prazo_manifesto',
                  'foto_inspecao_2', 'data_inspecao2', 'horario_inspecao2', 'data_manifesto', 'julgamento', 'situacao',
                  'rastreio_julgamento', 'status_rastreio_julgamento', 'data_entrega_julgamento', 'produtividade_infracao',
                  'produtividade_manifesto', 'email']

class FeriadoRecessoForm(forms.ModelForm):
    class Meta:
        model = FeriadoRecesso
        fields = ['data', 'descricao', 'tipo']


class InfracaoForm(forms.ModelForm):
    class Meta:
        model = Infracao
        fields = ['rastreio_infracao', 'status_rastreio', 'data_entrega_autuacao', 'nome_recebedor',
                  'prazo_defesa']

    def __init__(self, *args, **kwargs):
        super(InfracaoForm, self).__init__(*args, **kwargs)

        if self.fields is not None:
            self.helper = FormHelper()
            self.helper.layout = Layout(*[field for field in self.fields if field != 'data_entrega_autuacao'])
        else:
            raise ValueError("self.fields is None. It should be a dictionary containing the form fields.")


class InfracaoFormDefesa(forms.ModelForm):
    class Meta:
        model = Infracao
        fields = ['protocolo_defesa', 'entrada_protocolo', 'quem', 'prazo_manifesto',
                  'email']

    def __init__(self, *args, **kwargs):
        super(InfracaoFormDefesa, self).__init__(*args, **kwargs)

        if self.fields is not None:
            self.helper = FormHelper()
            self.helper.layout = Layout(*[field for field in self.fields if field != 'entrada_protocolo'])
        else:
            raise ValueError("self.fields is None. It should be a dictionary containing the form fields.")

class ARForm(forms.ModelForm):
    class Meta:
        model = Infracao
        fields = ['numero_format_ano','rastreio_infracao', 'status_rastreio', 'data_entrega_autuacao', 'nome_recebedor',
                  'prazo_defesa']

    def __init__(self, *args, **kwargs):
        super(ARForm, self).__init__(*args, **kwargs)

        if self.fields is not None:
            self.helper = FormHelper()
            self.helper.layout = Layout(*[field for field in self.fields if field != 'data_entrega_autuacao'])
        else:
            raise ValueError("self.fields is None. It should be a dictionary containing the form fields.")



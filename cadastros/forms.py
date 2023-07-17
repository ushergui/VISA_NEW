from django import forms
from .models import Logradouro, Bairro, Proprietario, Logradouro, Protocolo, Terreno, Inspecao, Infracao, FeriadoRecesso, ValorVRM
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.core.exceptions import ValidationError


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
        fields = ['inscricao','observacoes_terreno', 'logradouro_terreno', 'numero_terreno', 'complemento_terreno',
                  'proprietario', 'quadra', 'lote', 'area', 'logradouro_correspondencia',
                  'numero_correspondencia', 'complemento_correspondencia', 'tipo_de_imovel']

class TerrenoUpdateForm(forms.ModelForm):
    logradouro_terreno = forms.ModelChoiceField(queryset=Logradouro.objects.select_related('bairro__cidade__estado').all())
    logradouro_correspondencia = forms.ModelChoiceField(queryset=Logradouro.objects.select_related('bairro__cidade__estado').all())

    class Meta:
        model = Terreno
        fields = ['inscricao','observacoes_terreno', 'logradouro_terreno', 'numero_terreno', 'complemento_terreno',
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

class ReinspecaoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            if instance.status_rastreio != 'ENTREGUE':
                self.fields['situacao'].choices = (
                    ("", "---------"),
                    ("6", "Não recebeu e limpou"),
                    ("4", "Manifesto e julgamento fora do sistema"),
                    ("11", "Erro na identificação")
                    
                )
            elif instance.status_rastreio == 'ENTREGUE' and not instance.protocolo_defesa:
                self.fields['situacao'].choices = (
                    ("", "---------"),
                    ("2", "Não defendeu e limpou"),
                    ("13", "Não defendeu e limpou (razoável)"),
                    ("3", "Não defendeu e não limpou"),
                    ("4", "Manifesto e julgamento fora do sistema"),
                    ("8", "Não defendeu e não limpou via Edital"),
                    ("9", "Não defendeu e limpou via Edital"),
                    ("15", "Não defendeu e limpou (razoável) via Edital"),
                    ("10", "Perda de prazo"),
                    ("11", "Erro na identificação")
                    
                )
            elif instance.status_rastreio == 'ENTREGUE' and instance.protocolo_defesa:
                self.fields['situacao'].choices = (
                    ("", "---------"),
                    ("1", "Defendeu e limpou"),
                    ("14", "Defendeu e limpou (razoável)"),
                    ("4", "Manifesto e julgamento fora do sistema"),
                    ("5", "Defendeu após o prazo e limpou"),
                    ("10", "Perda de prazo"),
                    ("11", "Erro na identificação"),
                    ("12", "Mudança do proprietário no decorrer do processo"),
                    ("16", "Defendeu e indicou possuidor")
                )
            else:
                self.fields['situacao'].choices = (
                    ("", "---------"),
                    ("4", "Manifesto e julgamento fora do sistema"),
                    ("10", "Perda de prazo"),
                    ("11", "Erro na identificação"),
                    ("12", "Mudança do proprietário no decorrer do processo"),
                )

    class Meta:
        model = Infracao
        fields = ['numero_format_ano', 'foto_inspecao_2', 'data_inspecao2', 'horario_inspecao2', 'data_manifesto',
                  'produtividade_manifesto', 'situacao', 'julgamento']

    def clean(self):
        cleaned_data = super().clean()
        situacao = cleaned_data.get('situacao')
        data_manifesto = cleaned_data.get('data_manifesto')
        julgamento = cleaned_data.get('julgamento')
        data_inspecao2 = cleaned_data.get('data_inspecao2')
        produtividade_manifesto = cleaned_data.get('produtividade_manifesto')

        # Checar se a situacao foi preenchida e se as datas foram deixadas em branco
        if situacao and situacao != "" and (not data_manifesto or not julgamento):
            raise forms.ValidationError(
                "As datas de manifesto e julgamento são obrigatórias quando uma situação é selecionada."
            )

        # Checar se a data do manifesto é posterior ao julgamento
        if data_manifesto and julgamento and data_manifesto > julgamento:
            raise forms.ValidationError(
                "A data do manifesto não pode ser posterior à data do julgamento."
            )

        # Checar se a data_inspecao2 é maior que a data_manifesto
        if data_inspecao2 and data_manifesto and data_inspecao2 > data_manifesto:
            raise forms.ValidationError(
                "A data da inspeção não pode ser posterior à data do manifesto."
            )
        
        # Checar se a produtividade_manifesto é menor que a data_manifesto
        if produtividade_manifesto and data_manifesto and produtividade_manifesto < data_manifesto:
            raise forms.ValidationError(
                "A data da produtividade não pode ser inferior a data do manifesto."
            )
        
        return cleaned_data

    def clean_situacao(self):
        situacao = self.cleaned_data.get('situacao')

        if not situacao:
            raise forms.ValidationError("Escolha uma situação válida.")
        return situacao


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


class ValorVRMForm(forms.ModelForm):
    class Meta:
        model = ValorVRM
        fields = ['ano', 'valor']
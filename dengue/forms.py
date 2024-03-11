from django import forms
from .models import Notificacao, Semana
from cadastros.models import Cidade, Bairro, Logradouro

class LogradouroModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.tipo} {obj.nome_logradouro} - {obj.bairro.nome_bairro}"

class SemanaModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.semana} - {obj.ano}"

class NotificacaoForm(forms.ModelForm):
    logradouro_paciente = LogradouroModelChoiceField(queryset=Logradouro.objects.select_related('bairro', 'bairro__cidade').all())
    semana_epidemiologica = SemanaModelChoiceField(queryset=Semana.objects.all(), empty_label="Selecione a semana epidemiológica")
    class Meta:
        model = Notificacao
        fields = [
            'nome',
            'telefone',
            'logradouro_paciente',
            'numero_paciente',
            'usf',
            'data_recebimento',
            'notificadora',
            'data_notificacao',
            'data_inicio_sintomas',
            'data_limite_coleta',
            'semana_epidemiologica',
            'sinan',
            'grupo_estimado',
            'resultado',
            'internacao',
            'obito',
            'status_obito',
            'data_agendamento',
            'observacoes',
            'classificacao',
            'motivo_encerramento',
            'evolucao',
            'data_encerramento',
        ]

    def __init__(self, *args, **kwargs):
        super(NotificacaoForm, self).__init__(*args, **kwargs)
        cidade_ss_paraiso = Cidade.objects.filter(nome_cidade="SAO SEBASTIAO DO PARAISO").first()

        if cidade_ss_paraiso:
            bairros_ss_paraiso = Bairro.objects.filter(cidade=cidade_ss_paraiso)
            logradouros_ss_paraiso = Logradouro.objects.filter(bairro__in=bairros_ss_paraiso)
            self.fields['logradouro_paciente'].queryset = logradouros_ss_paraiso
        else:
            self.fields['logradouro_paciente'].queryset = Logradouro.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get("nome")
        logradouro_paciente = cleaned_data.get("logradouro_paciente")

        return cleaned_data

class SemanaForm(forms.ModelForm):
    class Meta:
        model = Semana
        fields = ['semana', 'ano','data_inicio_semana', 'data_fim_semana']

class EncerrarNotificacaoForm(forms.ModelForm):
    class Meta:
        model = Notificacao
        fields = [
            'nome',
            'logradouro_paciente',
            'numero_paciente',
            'usf',
            'data_notificacao',
            'data_inicio_sintomas',
            'semana_epidemiologica',
            'sinan',
            'resultado',
            'internacao',
            'obito',
            'data_agendamento',
            'observacoes',
            'classificacao',
            'motivo_encerramento',
            'evolucao',
            'data_encerramento',
        ]
        #widgets = {
        #    'motivo_encerramento': forms.RadioSelect,
        #    'classificacao': forms.RadioSelect,
        #    'evolucao': forms.RadioSelect
       # }


    def clean(self):
        cleaned_data = super().clean()
        data_encerramento = cleaned_data.get('data_encerramento')
        data_notificacao = cleaned_data.get('data_notificacao')
        motivo_encerramento = cleaned_data.get('motivo_encerramento')

        if data_encerramento and not motivo_encerramento:
            self.add_error('motivo_encerramento', 'Por favor, selecione o motivo do encerramento.')
        elif motivo_encerramento and not data_encerramento:
            self.add_error('data_encerramento', 'Por favor, preencha a data do encerramento.')
        elif data_encerramento and data_notificacao and data_encerramento < data_notificacao:
            self.add_error('data_encerramento', 'A data de encerramento não pode ser inferior à data de notificação.')


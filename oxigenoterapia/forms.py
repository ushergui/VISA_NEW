from django import forms
from .models import Paciente, Fisioterapeuta, Equipamento, Descartavel, Cid, ModoDeUso, Usf, Atendimento, Prescricao, Finalidade
from cadastros.models import Cidade, Bairro, Logradouro
from django.core.exceptions import ValidationError

class LogradouroModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.tipo} {obj.nome_logradouro} - {obj.bairro.nome_bairro}"

class PacienteForm(forms.ModelForm):
    logradouro_paciente = LogradouroModelChoiceField(queryset=Logradouro.objects.select_related('bairro', 'bairro__cidade').all(), label='Endereço')
   
    class Meta:
        model = Paciente
        fields = '__all__'  # Usamos todos os campos do modelo Paciente

       

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        self.fields['prontuario_paciente'].widget.attrs['placeholder'] = 'Digite somente números'
        self.fields['nascimento_paciente'].widget.attrs['placeholder'] = '__/__/____'
        self.fields['telefone_paciente1'].widget.attrs['placeholder'] = 'Celular ou fixo'
        self.fields['telefone_paciente2'].widget.attrs['placeholder'] = 'Celular ou fixo'
        self.fields['rg_paciente'].widget.attrs['placeholder'] = 'Somente números'
        self.fields['cpf_paciente'].widget.attrs['placeholder'] = '000.000.000-00'
        cidade_ss_paraiso = Cidade.objects.filter(nome_cidade="SAO SEBASTIAO DO PARAISO").first()

        if cidade_ss_paraiso:
            bairros_ss_paraiso = Bairro.objects.filter(cidade=cidade_ss_paraiso)
            logradouros_ss_paraiso = Logradouro.objects.filter(bairro__in=bairros_ss_paraiso)
            self.fields['logradouro_paciente'].queryset = logradouros_ss_paraiso
        else:
            self.fields['logradouro_paciente'].queryset = Logradouro.objects.none()
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        data_obito = cleaned_data.get('data_obito')
        data_alta = cleaned_data.get('data_alta')

        if status == 'ÓBITO' and not data_obito:
            self.add_error('data_obito', ValidationError(
                'Favor preencher o campo de data de óbito.',
                code='required',
            ))

        if status == 'ALTA' and not data_alta:
            self.add_error('data_alta', ValidationError(
                'Favor preencher o campo de data de alta.',
                code='required',
            ))

        if data_obito and status != 'ÓBITO':
            self.add_error('status', ValidationError(
                'Favor selecionar o campo ÓBITO no status.',
                code='invalid',
            ))

        if data_alta and status != 'ALTA':
            self.add_error('status', ValidationError(
                'Favor selecionar o campo ALTA no status.',
                code='invalid',
            ))


class FisioterapeutaForm(forms.ModelForm):
    class Meta:
        model = Fisioterapeuta
        fields = '__all__'

class FinalidadeForm(forms.ModelForm):
    class Meta:
        model = Finalidade
        fields = '__all__'

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = '__all__'


class DescartavelForm(forms.ModelForm):
    class Meta:
        model = Descartavel
        fields = '__all__'

class CidForm(forms.ModelForm):
    class Meta:
        model = Cid
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(CidForm, self).__init__(*args, **kwargs)
        self.fields['codigo_doenca'].widget.attrs['placeholder'] = 'Exemplo: J43.9'
        self.fields['nome_doenca'].widget.attrs['placeholder'] = 'Somente letras'


class PrescricaoForm(forms.ModelForm):
    class Meta:
        model = Prescricao
        fields = ['paciente', 'equipamento', 'data_inicio_uso', 'tempo_de_uso', 'cid', 'litros', 'parametros', 'status', 'numero_oficio', 'data_oficio','destinatario_oficio']

class ModoDeUsoForm(forms.ModelForm):
    class Meta:
        model = ModoDeUso
        fields = ['paciente', 'equipamento', 'data_inicio_uso', 'tempo_de_uso', 'cid', 'litros', 'parametros', 'status']

class AtendimentoForm(forms.ModelForm):
    equipamento = forms.ModelMultipleChoiceField(queryset=Equipamento.objects.all(), required=False)
    tempo_de_uso = forms.ChoiceField(choices=[('', '---------')] + list(ModoDeUso.TEMPO_USO_CHOICES), required=False)
    litros = forms.CharField(max_length=50, required=False)
    parametros = forms.CharField(max_length=300, required=False)

    class Meta:
        model = Atendimento
        fields = ['prescricao', 'data_atendimento', 'troca_de_filtro', 'troca_de_mascara', 'relatorio_atendimento', 'fisioterapeuta_atendimento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prescricao'].disabled = True
        self.fields['prescricao'].empty_label = None


        if self.instance.pk:
            # Obter o objeto Prescricao relacionado 
            mododeuso = self.instance.prescricao

            # Configurar os valores iniciais dos campos com os valores atuais da prescricao
            self.fields['equipamento'].initial = mododeuso.equipamento.all()
            self.fields['tempo_de_uso'].initial = mododeuso.tempo_de_uso
            self.fields['litros'].initial = mododeuso.litros
            self.fields['parametros'].initial = mododeuso.parametros

        # Define o widget para botões do tipo "radio"
        self.fields['troca_de_filtro'].widget = forms.RadioSelect(choices=[(True, 'Sim'), (False, 'Não')])
        self.fields['troca_de_mascara'].widget = forms.RadioSelect(choices=[(True, 'Sim'), (False, 'Não')])
    
    def clean(self):
        cleaned_data = super().clean()
        data_atendimento = cleaned_data.get('data_atendimento')
        prescricao = cleaned_data.get('prescricao')

        if data_atendimento and prescricao and data_atendimento < prescricao.data_inicio_uso:
            raise ValidationError("A data do atendimento não pode ser anterior à data de início do uso.")

class UsfForm(forms.ModelForm):
    class Meta:
        model = Usf
        fields = '__all__'
from django import forms
from .models import Contabilidade, Cnae, Empresas, Risco

class ContabilidadeForm(forms.ModelForm):
    class Meta:
        model = Contabilidade
        fields = '__all__'

class CnaeForm(forms.ModelForm):
    class Meta:
        model = Cnae
        fields = '__all__'

class EmpresasForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = '__all__'


class RiscoForm(forms.ModelForm):
    class Meta:
        model = Risco
        fields = ['risco', 'valor_risco']
from django.shortcuts import render
from oxigenoterapia.models import Fisioterapeuta

#Importar o TemplateView para criar páginas simples
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin



#A classe PaginaInicial "extends" TemplateView. Ela serve basicamente para renderizar HTML
class PaginaInicial(LoginRequiredMixin, TemplateView):
    #Toda classe filha do TemplateView precisa do atributo abaixo para ser renderizado
    template_name = "index2.html"

class PaginaInicial3(LoginRequiredMixin, TemplateView):
    #Toda classe filha do TemplateView precisa do atributo abaixo para ser renderizado
    template_name = "dengue/index_dengue.html"

class PaginaInicial4(LoginRequiredMixin, TemplateView):
    #Toda classe filha do TemplateView precisa do atributo abaixo para ser renderizado
    template_name = "oxigenoterapia/index_oxigenoterapia.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fisioterapeutas'] = Fisioterapeuta.objects.all()
        return context



class SobreView(TemplateView):
    template_name = 'sobre.html'

class EmpresasView(TemplateView):
    template_name = 'empresas/empresas.html'

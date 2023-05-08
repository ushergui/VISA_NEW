from django.shortcuts import render

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



class SobreView(TemplateView):
    template_name = 'sobre.html'

class EmpresasView(TemplateView):
    template_name = 'empresas/empresas.html'

from django.shortcuts import render

#Importar o TemplateView para criar páginas simples
from django.views.generic import TemplateView



#A classe PaginaInicial "extends" TemplateView. Ela serve basicamente para renderizar HTML
class PaginaInicial(TemplateView):
    #Toda classe filha do TemplateView precisa do atributo abaixo para ser renderizado
    template_name = "index2.html"



class SobreView(TemplateView):
    template_name = 'sobre.html'

from django.urls import path #Estou pegando do módulo django
from .views import PaginaInicial, SobreView #O ponto no início significa que está pegando um arquivo dentro daquele diretório

#padrão de url que tem lá na outra url, ele funciona como se fosse um vetor

urlpatterns = [
    path('', PaginaInicial.as_view(), name='index'), #O que o usuário vai digitar pra acessar a página, qual a
    # view que vai ser chamada e por último um nome para url
    #path('endereço', minha-view.as_view(), name='nome-da-url'),
    path('sobre/', SobreView.as_view(), name='sobre')

]
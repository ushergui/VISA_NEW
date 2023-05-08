from django.contrib import admin, messages
from django.urls import path
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse

# Importar as classes
from .models import Estado, Cidade, Bairro, Logradouro, Proprietario, Terreno, Inspecao, Infracao, Protocolo, Fiscal

admin.site.register(Inspecao)
admin.site.register(Terreno)
admin.site.register(Proprietario)
admin.site.register(Logradouro)
admin.site.register(Bairro)
admin.site.register(Cidade)
admin.site.register(Estado)
admin.site.register(Protocolo)
admin.site.register(Fiscal)
admin.site.register(Infracao)

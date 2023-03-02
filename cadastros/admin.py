from django.contrib import admin

# Importar as classes
from .models import Estado, Cidade, Bairro, Logradouro, Proprietario, Terreno

admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Bairro)
admin.site.register(Logradouro)
admin.site.register(Proprietario)
admin.site.register(Terreno)


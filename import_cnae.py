import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Vigilancia.settings')
django.setup()

from empresas.models import Cnae, Risco, Legislacao

with open('CNAESS.csv', 'r', encoding='UTF8') as f:
    reader = csv.reader(f)
    next(reader)  # pular o cabeçalho
    for row in reader:
        # Obter a instância de Risco e Legislacao correspondente
        risco = Risco.objects.get(pk=row[4])
        legislacao = Legislacao.objects.get(pk=row[3])
        
        # Criar um novo objeto Cnae
        cnae = Cnae(
            codigo_cnae=row[0], 
            descricao_cnae=row[1], 
            observacoes_cnae=row[2] if row[2] else None, 
            risco_cnae=risco
        )
        cnae.save()
        # Adicionar a relação many-to-many com Legislacao
        cnae.legislacao.add(legislacao)

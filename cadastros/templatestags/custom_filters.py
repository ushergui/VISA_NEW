from django import template
from django.utils.text import capfirst

register = template.Library()

MONTHS_PT_BR = {
    1: 'janeiro',
    2: 'fevereiro',
    3: 'março',
    4: 'abril',
    5: 'maio',
    6: 'junho',
    7: 'julho',
    8: 'agosto',
    9: 'setembro',
    10: 'outubro',
    11: 'novembro',
    12: 'dezembro',
}

def capitalize_name(name):
    # lista de artigos que devem ser mantidos em minúsculo
    articles = ['de', 'da', 'do', 'das', 'dos']

    # lista de números romanos que devem ser mantidos em maiúsculo
    roman_numerals = ['II', 'III', 'VI', 'VII', 'XIII', 'XXIII', 'IV', 'LTDA']

    # separa o nome em palavras
    words = name.split(' ')

    # percorre cada palavra
    for i, word in enumerate(words):
        # verifica se a palavra é um artigo
        if word.lower() in articles:
            # coloca o artigo em minúsculo
            words[i] = word.lower()
        # verifica se a palavra é um número romano
        elif word.upper() in roman_numerals:
            # mantém o número romano em maiúsculo
            words[i] = word.upper()
        else:
            # coloca a primeira letra da palavra em maiúsculo e o restante em minúsculo
            words[i] = capfirst(word.lower())

    # junta as palavras novamente e retorna o nome formatado
    return ' '.join(words)

@register.filter
def month_lower(date):
    if date:
        month = MONTHS_PT_BR[date.month]
        return date.strftime('%d de ') + month + date.strftime(' de %Y')
    return 'Data não disponível'

register.filter('capitalize_name', capitalize_name)

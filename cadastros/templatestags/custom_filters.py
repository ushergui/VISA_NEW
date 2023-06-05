from django import template
from django.utils.text import capfirst

register = template.Library()

def capitalize_name(name):
    # lista de artigos que devem ser mantidos em minúsculo
    articles = ['de', 'da', 'do', 'das', 'dos']

    # lista de números romanos que devem ser mantidos em maiúsculo
    roman_numerals = ['II', 'III', 'VI', 'VII', 'XIII', 'XXIII', 'IV']

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

register.filter('capitalize_name', capitalize_name)


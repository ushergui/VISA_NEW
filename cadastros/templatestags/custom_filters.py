
from django import template
from django.utils.text import capfirst

register = template.Library()

def capitalize_name(name):
    # lista de artigos que devem ser mantidos em minúsculo
    articles = ['de', 'da', 'do', 'das', 'dos']

    # separa o nome em palavras
    words = name.split(' ')

    # percorre cada palavra
    for i, word in enumerate(words):
        # verifica se a palavra é um artigo
        if word.lower() in articles:
            # coloca o artigo em minúsculo
            words[i] = word.lower()
        else:
            # coloca a primeira letra da palavra em maiúsculo e o restante em minúsculo
            words[i] = capfirst(word.lower())

    # junta as palavras novamente e retorna o nome formatado
    return ' '.join(words)

register.filter('capitalize_name', capitalize_name)

from django import template
from crispy_forms.utils import TEMPLATE_PACK

register = template.Library()

@register.filter(name='crispy_without_data_entrega_autuacao')
def crispy_without_data_entrega_autuacao(form, template_pack=TEMPLATE_PACK):
    fields = [field for field in form if field.name != 'data_entrega_autuacao']
    helper = form.helper
    form.helper = None
    html = ''
    for field in fields:
        html += field.as_widget()
    form.helper = helper
    return html

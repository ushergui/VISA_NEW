from django import template

register = template.Library()

@register.simple_tag
def form_field(form, field_name):
    return form[field_name]

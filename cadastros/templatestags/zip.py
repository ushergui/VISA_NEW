from django import template

register = template.Library()

@register.filter
def zip_lists(a, b):
    return zip(a, b)

@register.filter
def get_field(form, field_name):
    return form.fields[field_name]

@register.filter
def get_item(queryset, id):
    return queryset.filter(id=id).first()
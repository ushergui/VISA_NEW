from django import template
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
import os

register = template.Library()

@register.filter
def to_absolute_url(value):
    if value:
        return os.path.join('file://', os.path.abspath(staticfiles_storage.path(value)))
    return ''


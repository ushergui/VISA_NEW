from django.apps import AppConfig

class CadastrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cadastros'

    def ready(self):
        import cadastros.templatestags.custom_filters
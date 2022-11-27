from django.apps import AppConfig


class GeneralAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'general_app'

    def ready(self):
        print('ready()')
        from . import updater
        updater.start()
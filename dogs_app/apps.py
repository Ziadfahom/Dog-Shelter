from django.apps import AppConfig


class DogsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dogs_app'

    # Use signals defined in the models.py
    def ready(self):
        import dogs_app.signals

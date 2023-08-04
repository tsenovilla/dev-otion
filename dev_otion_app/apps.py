from django.apps import AppConfig

class DevOtionAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dev_otion_app"

    def ready(self):
        from . import signals
        return super().ready()

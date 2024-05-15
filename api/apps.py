from django.apps import AppConfig
from api.firebase_config import MyAppConfig


class MindSupportConfig(AppConfig):
    name = "mindsupport"

    def ready(self):
        MyAppConfig.ready(self)

from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'User'

    def ready(self):
        from . import signals

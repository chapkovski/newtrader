from django.apps import AppConfig


class TWConfig(AppConfig):
    name = 'trader_wrapper'

    def ready(self):
        from . import signals  # noqa

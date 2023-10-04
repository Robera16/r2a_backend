from django.apps import AppConfig


class ApiAuthConfig(AppConfig):
    name = 'api_auth'

    def ready(self):
        import api_auth.signals
from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = 'pages'

    # get signals
    def ready(self):
        import pages.signals
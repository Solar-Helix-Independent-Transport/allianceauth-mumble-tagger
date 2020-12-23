from django.apps import AppConfig

class MumbleTaggerConfig(AppConfig):
    name = 'mumbletagger'
    label = 'mumbletagger'
    verbose_name = 'Mumble Tagger'

    def ready(self):
        import mumbletagger.signals

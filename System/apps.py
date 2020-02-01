from django.apps import AppConfig


class SystemConfig(AppConfig):
    name = 'System'

    def ready(self):
    	import System.signals
from django.apps import AppConfig

class MembersConfig(AppConfig):
    name = 'members'

    def ready(self):
        from .groups import create_groups
        create_groups()

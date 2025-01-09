from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

def create_groups():
    """
    Create default user groups if they don't already exist.
    """
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='Trainer')
    Group.objects.get_or_create(name='Member')

@receiver(post_migrate)
def create_groups_after_migration(sender, **kwargs):
    """
    Ensure groups are created after migrations are applied.
    """
    create_groups()

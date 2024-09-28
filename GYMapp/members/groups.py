from django.contrib.auth.models import Group

def create_groups():
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='Trainer')
    Group.objects.get_or_create(name='Member')

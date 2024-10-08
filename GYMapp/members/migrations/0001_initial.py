# Generated by Django 5.1 on 2024-09-01 11:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('packages', '0001_initial'),
        ('trainer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=20)),
                ('sarting_date', models.DateTimeField(auto_now_add=True)),
                ('dob', models.DateTimeField()),
                ('delete_status', models.IntegerField(choices=[(1, 'Live'), (0, 'Delete')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='package', to='packages.packages')),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trainer', to='trainer.trainer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

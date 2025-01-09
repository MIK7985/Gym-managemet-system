# Generated by Django 5.1 on 2024-10-15 15:26

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
        ('members', '0008_member_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='user',
        ),
        migrations.AddField(
            model_name='attendance',
            name='check_in_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='check_out_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='attendance',
            name='member',
            field=models.ForeignKey(default=19, on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='members.member'),
        ),
        migrations.DeleteModel(
            name='Fingerprint',
        ),
    ]

# Generated by Django 5.1.4 on 2025-01-11 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0007_alter_workout_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='workouts/videos/'),
        ),
    ]

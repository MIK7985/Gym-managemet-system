# Generated by Django 5.1.4 on 2025-01-11 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0002_workout_day_alter_workout_title_alter_workout_video_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workout',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='workout',
            name='day',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='workout',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='workout',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='workout_videos/'),
        ),
    ]

# Generated by Django 5.1.4 on 2025-01-11 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_alter_member_trainer'),
        ('trainer', '0001_initial'),
        ('workouts', '0004_remove_workout_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='day',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='workout',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='workout',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='workouts/videos/'),
        ),
        migrations.AlterUniqueTogether(
            name='workout',
            unique_together={('trainer', 'member', 'day')},
        ),
    ]

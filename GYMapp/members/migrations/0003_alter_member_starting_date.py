# Generated by Django 5.1 on 2024-09-03 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_remove_member_sarting_date_member_starting_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='starting_date',
            field=models.DateField(),
        ),
    ]

# Generated by Django 5.1 on 2024-09-07 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_alter_member_dob_alter_member_starting_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='starting_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
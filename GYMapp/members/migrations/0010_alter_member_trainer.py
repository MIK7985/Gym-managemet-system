# Generated by Django 5.1.4 on 2025-01-11 08:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_member_package_expiry_date_member_qr_code_and_more'),
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='trainer.trainer'),
        ),
    ]

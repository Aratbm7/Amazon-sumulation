# Generated by Django 4.1.1 on 2022-09-19 08:00

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_mobileproduction_connect_tecnology'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobileproduction',
            name='colors',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10, null=True), size=8), blank=True, null=True, size=8),
        ),
    ]

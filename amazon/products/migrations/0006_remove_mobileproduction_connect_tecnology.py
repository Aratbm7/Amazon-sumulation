# Generated by Django 4.1.1 on 2022-09-19 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_mobileproduction_merchat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobileproduction',
            name='connect_tecnology',
        ),
    ]

# Generated by Django 4.1.1 on 2022-09-18 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '__first__'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobileproduction',
            name='merchat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='products', to='accounts.merchant'),
            preserve_default=False,
        ),
    ]

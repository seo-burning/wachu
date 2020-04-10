# Generated by Django 2.2.6 on 2020-04-10 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_auto_20200408_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='store_type',
            field=models.CharField(choices=[('IF', 'Instagram Facebook'), ('IF(P)', 'Instagram Facebook with price info'), ('IH', 'Instagram Homepage'), ('IS', 'Instagram Shopee'), ('IFS', 'Instagram Facebook Shopee')], default='IF', max_length=25),
        ),
    ]

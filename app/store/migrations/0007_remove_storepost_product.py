# Generated by Django 2.2.3 on 2019-07-29 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_storepost_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storepost',
            name='product',
        ),
    ]
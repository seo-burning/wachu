# Generated by Django 2.2.3 on 2019-08-26 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_storepost_is_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='store',
            options={'ordering': ('current_ranking',)},
        ),
    ]
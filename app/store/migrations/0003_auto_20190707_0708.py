# Generated by Django 2.2.3 on 2019-07-07 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20190705_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='tpo',
        ),
        migrations.DeleteModel(
            name='Tpo',
        ),
    ]

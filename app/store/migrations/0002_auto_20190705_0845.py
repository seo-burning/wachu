# Generated by Django 2.2.3 on 2019-07-05 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storepost',
            name='main_section_published',
        ),
        migrations.RemoveField(
            model_name='storepost',
            name='sliding_section_published',
        ),
    ]

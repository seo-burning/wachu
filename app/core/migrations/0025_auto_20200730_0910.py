# Generated by Django 3.0.8 on 2020-07-30 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_appleclienttoken'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appleclienttoken',
            old_name='clien_token',
            new_name='client_token',
        ),
    ]

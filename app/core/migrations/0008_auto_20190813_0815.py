# Generated by Django 2.2.3 on 2019-08-13 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_userpushtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpushtoken',
            name='push_token',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

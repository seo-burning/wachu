# Generated by Django 2.2.3 on 2019-08-06 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20190729_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_new_post',
            field=models.BooleanField(default=False),
        ),
    ]

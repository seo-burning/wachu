# Generated by Django 3.0.6 on 2020-05-19 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20200519_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='slug',
            field=models.SlugField(blank=True, max_length=5),
        ),
    ]

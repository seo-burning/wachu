# Generated by Django 3.0.6 on 2020-07-13 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0051_auto_20200713_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='validation_string',
            field=models.CharField(default='None/None/None/None', max_length=100),
        ),
    ]
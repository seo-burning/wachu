# Generated by Django 3.0.6 on 2020-06-02 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0043_auto_20200602_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='insta_id',
            field=models.CharField(max_length=255, unique=True, verbose_name='Instagram ID'),
        ),
    ]

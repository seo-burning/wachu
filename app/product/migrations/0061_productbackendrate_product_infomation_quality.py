# Generated by Django 2.2.6 on 2020-04-29 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0060_productbackendrate'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbackendrate',
            name='product_infomation_quality',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

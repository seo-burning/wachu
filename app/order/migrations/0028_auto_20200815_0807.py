# Generated by Django 3.0.9 on 2020-08-15 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0027_auto_20200813_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_price',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='orderedproduct',
            name='shipping_price',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='ordergroup',
            name='shipping_price',
            field=models.IntegerField(default=None, null=True),
        ),
    ]

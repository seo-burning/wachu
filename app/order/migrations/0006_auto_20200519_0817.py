# Generated by Django 3.0.6 on 2020-05-19 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='shipping_price',
            field=models.IntegerField(default=0),
        ),
    ]
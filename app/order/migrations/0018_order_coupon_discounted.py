# Generated by Django 3.0.6 on 2020-06-03 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_auto_20200531_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_discounted',
            field=models.IntegerField(default=0),
        ),
    ]

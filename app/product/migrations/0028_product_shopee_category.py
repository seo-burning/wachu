# Generated by Django 2.2.6 on 2020-04-17 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_shopeecategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shopee_category',
            field=models.ManyToManyField(blank=True, to='product.ShopeeCategory'),
        ),
    ]
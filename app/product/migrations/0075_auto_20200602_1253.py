# Generated by Django 3.0.6 on 2020-06-02 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0074_auto_20200601_0500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_source',
            field=models.CharField(choices=[('SHOPEE', 'Shopee'), ('INSTAGRAM', 'Instagram'), ('HOMEPAGE', 'Homepage'), ('DOSIIN', 'Dosi-in')], max_length=255),
        ),
    ]

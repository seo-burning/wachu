# Generated by Django 2.2.6 on 2020-04-17 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_auto_20200417_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_source',
            field=models.CharField(choices=[('SHOPEE', 'Shopee'), ('INSTAGRAM', 'Instagram'), ('HOMEPAGE', 'Homepage')], max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='size_chart',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]

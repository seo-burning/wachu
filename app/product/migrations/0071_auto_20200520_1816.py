# Generated by Django 3.0.6 on 2020-05-20 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0070_auto_20200520_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoption',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_options', to='product.Product'),
        ),
    ]

# Generated by Django 2.2.6 on 2020-04-17 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_auto_20200417_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopeerating',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Product'),
        ),
    ]

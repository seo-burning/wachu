# Generated by Django 2.2.3 on 2019-10-01 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20190930_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storepost',
            name='is_product',
            field=models.CharField(choices=[('P', 'Product'), ('E', 'Prodcut Etc'), ('N', 'NOT Product')], default='P', max_length=25),
        ),
    ]

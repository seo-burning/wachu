# Generated by Django 2.2.3 on 2019-09-26 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_product_ic_checked'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='ic_checked',
            new_name='is_checked',
        ),
    ]

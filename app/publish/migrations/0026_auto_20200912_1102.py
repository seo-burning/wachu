# Generated by Django 3.0.9 on 2020-09-12 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0099_auto_20200815_0822'),
        ('publish', '0025_auto_20200912_1100'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostGroup',
            new_name='ProductGroup',
        ),
    ]
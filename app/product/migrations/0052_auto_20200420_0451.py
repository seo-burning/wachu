# Generated by Django 2.2.6 on 2020-04-20 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0051_auto_20200419_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='display_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productstyle',
            name='display_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productsubcategory',
            name='display_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producttag',
            name='display_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]

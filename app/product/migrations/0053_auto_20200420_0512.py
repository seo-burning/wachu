# Generated by Django 2.2.6 on 2020-04-20 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0052_auto_20200420_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='display_name',
            field=models.CharField(default='Need to tranlate', max_length=255),
        ),
        migrations.AlterField(
            model_name='productsize',
            name='display_name',
            field=models.CharField(default='Need to tranlate', max_length=255),
        ),
        migrations.AlterField(
            model_name='productsubcategory',
            name='display_name',
            field=models.CharField(default='Need to tranlate', max_length=255),
        ),
    ]

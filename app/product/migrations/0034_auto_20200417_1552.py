# Generated by Django 2.2.6 on 2020-04-17 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0033_productcolor_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcolor',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Product Color'),
        ),
    ]

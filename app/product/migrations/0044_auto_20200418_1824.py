# Generated by Django 2.2.6 on 2020-04-18 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_auto_20200418_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsize',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Product Size'),
        ),
        migrations.AlterField(
            model_name='productsize',
            name='display_name',
            field=models.CharField(max_length=255),
        ),
    ]

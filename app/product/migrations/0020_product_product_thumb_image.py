# Generated by Django 2.2.6 on 2020-04-10 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_auto_20200408_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_thumb_image',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Post Thumb Image'),
        ),
    ]

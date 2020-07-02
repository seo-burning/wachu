# Generated by Django 3.0.6 on 2020-07-01 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0085_product_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size_chart_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='size_chart',
            field=models.ImageField(blank=True, null=True, upload_to='size-chart/%Y/%m'),
        ),
    ]
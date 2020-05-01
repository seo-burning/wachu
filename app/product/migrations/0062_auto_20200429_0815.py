# Generated by Django 2.2.6 on 2020-04-29 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0061_productbackendrate_product_infomation_quality'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['current_product_backend_rating']},
        ),
        migrations.AddField(
            model_name='product',
            name='current_product_backend_rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
    ]
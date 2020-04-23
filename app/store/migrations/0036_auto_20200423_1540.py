# Generated by Django 2.2.6 on 2020-04-23 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_store_shopee_numeric_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='current_review_rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
    ]

# Generated by Django 2.2.6 on 2020-04-17 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_auto_20200417_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='shopee_rating',
        ),
        migrations.AddField(
            model_name='product',
            name='shopee_item_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='shopeerating',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Product'),
        ),
    ]

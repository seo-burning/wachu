# Generated by Django 3.0.6 on 2020-07-16 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0096_auto_20200711_1155'),
        ('core', '0019_auto_20200716_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='primary_style',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_on_primary_style', to='product.ProductStyle'),
        ),
        migrations.AddField(
            model_name='user',
            name='secondary_style',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_on_secondary_style', to='product.ProductStyle'),
        ),
    ]

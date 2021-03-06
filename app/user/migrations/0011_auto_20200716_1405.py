# Generated by Django 3.0.6 on 2020-07-16 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0096_auto_20200711_1155'),
        ('user', '0010_userstyletaste'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstyletaste',
            name='primary_style',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_style_tastes_on_primary_style', to='product.ProductStyle'),
        ),
        migrations.AlterField(
            model_name='userstyletaste',
            name='secondary_style',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_style_tastes_on_secondary_style', to='product.ProductStyle'),
        ),
    ]

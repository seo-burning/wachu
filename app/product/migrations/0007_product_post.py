# Generated by Django 2.2.3 on 2019-07-29 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_storepost_product'),
        ('product', '0006_auto_20190729_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.StorePost'),
        ),
    ]
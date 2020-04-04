# Generated by Django 2.2.6 on 2020-04-04 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_auto_20200404_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='region',
        ),
        migrations.AddField(
            model_name='storeaddress',
            name='region',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='store_address_set', to='store.Region'),
            preserve_default=False,
        ),
    ]

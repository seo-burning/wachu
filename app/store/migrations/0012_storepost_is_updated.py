# Generated by Django 2.2.3 on 2019-08-26 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_storeranking_store_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='storepost',
            name='is_updated',
            field=models.BooleanField(default=False),
        ),
    ]

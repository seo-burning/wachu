# Generated by Django 3.0.8 on 2020-07-26 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0005_pick_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='pick',
            name='image_outlink',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]

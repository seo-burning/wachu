# Generated by Django 2.2.6 on 2020-04-19 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0050_auto_20200419_1503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='video_sourcee',
            new_name='video_source',
        ),
    ]
# Generated by Django 2.2.6 on 2020-04-12 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_user_favorite_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='favorite_product',
            new_name='favorite_products',
        ),
    ]
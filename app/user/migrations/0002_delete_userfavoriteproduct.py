# Generated by Django 2.2.6 on 2020-04-12 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_user_favorite_product'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserFavoriteProduct',
        ),
    ]

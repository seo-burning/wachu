# Generated by Django 2.2.6 on 2020-04-17 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_auto_20200417_1100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopeerating',
            old_name='liked_count',
            new_name='shopee_liked_count',
        ),
        migrations.RenameField(
            model_name='shopeerating',
            old_name='rating_star',
            new_name='shopee_rating_star',
        ),
        migrations.RenameField(
            model_name='shopeerating',
            old_name='review_count',
            new_name='shopee_review_count',
        ),
        migrations.RenameField(
            model_name='shopeerating',
            old_name='sold_count',
            new_name='shopee_sold_count',
        ),
        migrations.RenameField(
            model_name='shopeerating',
            old_name='view_count',
            new_name='shopee_view_count',
        ),
    ]

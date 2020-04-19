# Generated by Django 2.2.6 on 2020-04-19 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0049_auto_20200419_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image_type',
            field=models.CharField(choices=[('SP', 'Single Picture'), ('MP', 'Multiple Picture'), ('V', 'Video')], default='MP', max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='video_sourcee',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_thumbnail_image',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]

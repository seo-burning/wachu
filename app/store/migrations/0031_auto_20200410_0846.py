# Generated by Django 2.2.6 on 2020-04-10 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_auto_20200410_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='store_type',
            field=models.CharField(choices=[('IF', '-'), ('IF(P)', 'INS w/P'), ('IPFH', 'INS w/P HP'), ('IH', 'HP'), ('IS', 'Shopee'), ('IFSH', 'Shopee HP'), ('IF(P)SH', 'INS w/P SH')], default='IF', max_length=25, null=True),
        ),
    ]
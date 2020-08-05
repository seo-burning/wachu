# Generated by Django 3.0.9 on 2020-08-05 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_coupon_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_company',
            field=models.CharField(blank=True, choices=[('JT', 'J&T Express'), ('GHN', 'Giao Hàng Nhanh')], default=None, max_length=50, null=True, verbose_name='배송업체'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_tracking_code',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='배송조회 번호'),
        ),
    ]

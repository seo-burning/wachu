# Generated by Django 3.0.6 on 2020-05-20 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20200519_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('order-processing', '주문 완료'), ('delivery', '배송 중'), ('delivered', '배송 완료'), ('order-complete', '구매 완료'), ('cancelled', '주문 취소'), ('change-processing', '교환'), ('refund-processing', '환불'), ('refund-complete', '환불 완료')], default='order-processing', max_length=50, verbose_name='주문상태'),
        ),
        migrations.AlterField(
            model_name='orderstatuslog',
            name='order_status',
            field=models.CharField(choices=[('order-processing', '주문 완료'), ('delivery', '배송 중'), ('delivered', '배송 완료'), ('order-complete', '구매 완료'), ('cancelled', '주문 취소'), ('change-processing', '교환'), ('refund-processing', '환불'), ('refund-complete', '환불 완료')], default='order-processing', max_length=50, verbose_name='주문상태'),
        ),
    ]

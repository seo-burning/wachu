# Generated by Django 3.0.9 on 2020-08-16 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0030_order_estimated_delivery_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordergroupstatuslog',
            options={'ordering': ['-created_at', 'order_group'], 'verbose_name': '주문 그룹 상태', 'verbose_name_plural': '주문 그룹 상태'},
        ),
        migrations.RemoveField(
            model_name='ordergroupstatuslog',
            name='ordered_product',
        ),
        migrations.AddField(
            model_name='ordergroupstatuslog',
            name='order_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.OrderGroup', verbose_name='주문 제품 그룹'),
        ),
    ]
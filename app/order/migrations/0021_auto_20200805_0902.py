# Generated by Django 3.0.9 on 2020-08-05 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_auto_20200805_0839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderstatuslog',
            name='delivery_status',
        ),
        migrations.CreateModel(
            name='DeliveryStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_status', models.CharField(blank=True, max_length=50, verbose_name='배송상태')),
                ('status_timestamp', models.DateTimeField(blank=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.Order', verbose_name='주문서')),
            ],
        ),
    ]

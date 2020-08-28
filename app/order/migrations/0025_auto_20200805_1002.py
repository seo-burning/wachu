# Generated by Django 3.0.9 on 2020-08-05 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0024_auto_20200805_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_company',
            field=models.CharField(blank=True, choices=[('J&T Express', 'JT_Express'), ('Giao Hàng Nhanh', 'Giao_Hang_Nhanh')], default=None, max_length=50, null=True, verbose_name='배송업체'),
        ),
    ]
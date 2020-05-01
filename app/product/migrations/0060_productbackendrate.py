# Generated by Django 2.2.6 on 2020-04-29 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0059_auto_20200428_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBackEndRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_backend_rating', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('review_count', models.IntegerField(blank=True, null=True)),
                ('review_rate', models.FloatField(blank=True, null=True)),
                ('shopee_review_count', models.IntegerField(blank=True, null=True)),
                ('shopee_review_rate', models.FloatField(blank=True, null=True)),
                ('shopee_view_count', models.IntegerField(blank=True, null=True)),
                ('shopee_liked_count', models.IntegerField(blank=True, null=True)),
                ('shopee_sold_count', models.IntegerField(blank=True, null=True)),
                ('post_like', models.IntegerField(blank=True, null=True)),
                ('post_comment', models.IntegerField(blank=True, null=True)),
                ('app_click_count', models.IntegerField(blank=True, null=True)),
                ('app_outlink_count', models.IntegerField(blank=True, null=True)),
                ('user_favorite_count', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_backend_rating_set', to='product.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
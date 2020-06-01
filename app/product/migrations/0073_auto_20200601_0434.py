# Generated by Django 3.0.6 on 2020-06-01 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0072_auto_20200522_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('display_name', models.CharField(default='Need to tranlate', max_length=255)),
            ],
            options={
                'verbose_name': '제품 태그 / Product Tag',
                'verbose_name_plural': '제품 태그 / Product Tag',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(blank=True, to='product.ProductTag'),
        ),
    ]

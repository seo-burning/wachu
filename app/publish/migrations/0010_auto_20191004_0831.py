# Generated by Django 2.2.3 on 2019-10-04 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_auto_20190926_0836'),
        ('publish', '0009_linkingbanner_published_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postgroup',
            name='published_page',
        ),
        migrations.CreateModel(
            name='PostTagGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ordering', models.IntegerField(default=999, null=True)),
                ('product_number', models.IntegerField(default=10)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.ProductCategory')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.ProductColor')),
                ('published_banner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='publish.MainPagePublish')),
                ('style', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.ProductStyle')),
                ('sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.ProductSubCategory')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

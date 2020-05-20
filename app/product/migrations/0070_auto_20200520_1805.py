# Generated by Django 3.0.6 on 2020-05-20 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0069_product_shipping_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductTag',
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'ordering': ['ordering'], 'verbose_name': '제품 상위 카테고리 / Product Category', 'verbose_name_plural': '제품 상위 카테고리 / Product Category'},
        ),
        migrations.AlterModelOptions(
            name='productcolor',
            options={'verbose_name': '제품 색상 / Product Color', 'verbose_name_plural': '제품 색상 / Product Color'},
        ),
        migrations.AlterModelOptions(
            name='productsize',
            options={'verbose_name': '제품 사이즈 / Product Size', 'verbose_name_plural': '제품 사이즈 / Product Size'},
        ),
        migrations.AlterModelOptions(
            name='productsubcategory',
            options={'ordering': ['category', 'ordering'], 'verbose_name': '제품 하위 카테고리 / Product SubCategory', 'verbose_name_plural': '제품 하위 카테고리 / Product SubCategory'},
        ),
        migrations.AddField(
            model_name='productoption',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.ProductColor'),
        ),
        migrations.AddField(
            model_name='productoption',
            name='discount_rate',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productoption',
            name='extra_option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.ProductExtraOption'),
        ),
        migrations.AddField(
            model_name='productoption',
            name='is_free_ship',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productoption',
            name='shipping_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productoption',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.ProductSize'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='productcolor',
            name='display_name',
            field=models.CharField(default='Need to tranlate', max_length=255),
        ),
        migrations.AlterField(
            model_name='productcolor',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='productoption',
            name='currency',
            field=models.CharField(choices=[('VND', 'VND')], default='VND', max_length=20),
        ),
        migrations.AlterField(
            model_name='productsize',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='productsubcategory',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]

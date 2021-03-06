# Generated by Django 3.0.6 on 2020-06-29 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0083_auto_20200629_1826'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductSourceExtraOption',
            new_name='SourceExtraOption',
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at', 'current_product_backend_rating'], 'verbose_name': '제품 / Product', 'verbose_name_plural': '제품 / Product'},
        ),
        migrations.AlterModelOptions(
            name='sourceextraoption',
            options={'verbose_name': '소스 - 기타 옵션 / Product Source Extra Option', 'verbose_name_plural': '소스 - 기타 옵션 / Product Source Extra Option'},
        ),
    ]

# Generated by Django 2.2.3 on 2019-07-31 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0003_auto_20190731_0331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postgroup',
            name='published_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='publish.MainPagePublish'),
        ),
    ]

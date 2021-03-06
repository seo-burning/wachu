# Generated by Django 2.2.3 on 2019-08-28 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0004_auto_20190731_0534'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerPublish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('date', models.DateField(verbose_name='Published Date')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='postgroup',
            name='cover_picture',
            field=models.ImageField(blank=True, upload_to='post-group-cover/%Y/%m'),
        ),
        migrations.AddField(
            model_name='postgroup',
            name='published_banner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='publish.BannerPublish'),
        ),
    ]

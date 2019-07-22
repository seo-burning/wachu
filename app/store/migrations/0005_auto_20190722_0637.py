# Generated by Django 2.2.3 on 2019-07-22 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0004_auto_20190707_0816'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavoriteStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserFavoritePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('store_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.StorePost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='store',
            name='favorite_users',
            field=models.ManyToManyField(related_name='favorite_stores', through='store.UserFavoriteStore', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='storepost',
            name='favorite_users',
            field=models.ManyToManyField(related_name='favorite_posts', through='store.UserFavoritePost', to=settings.AUTH_USER_MODEL),
        ),
    ]

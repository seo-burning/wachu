# Generated by Django 2.2.6 on 2020-04-04 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0021_auto_20200404_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStoreReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='store',
            name='favorite_users',
            field=models.ManyToManyField(related_name='store_reviews', through='store.UserStoreReview', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userstorereview',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store'),
        ),
        migrations.AddField(
            model_name='userstorereview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

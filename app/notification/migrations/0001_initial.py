# Generated by Django 3.0.8 on 2020-07-23 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PushNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('user_scope', models.CharField(default='ALL', max_length=1000)),
                ('data', models.CharField(blank=True, max_length=1000)),
                ('title', models.CharField(max_length=100)),
                ('body', models.CharField(max_length=200)),
                ('ttl', models.IntegerField(blank=True)),
                ('expiration', models.IntegerField(blank=True)),
                ('priority', models.CharField(choices=[('default', 'default'), ('normal', 'normal'), ('high', 'high')], default='default', max_length=10)),
                ('subtitle', models.CharField(blank=True, max_length=100)),
                ('sound', models.CharField(choices=[('default', 'default'), ('null', None)], default='default', max_length=20, null=True)),
                ('badge', models.IntegerField(default=1)),
                ('channel_id', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

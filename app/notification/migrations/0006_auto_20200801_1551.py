# Generated by Django 3.0.8 on 2020-08-01 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0005_pushnotificationresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='badge',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='body',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usernotification',
            name='channel_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='data',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='expiration',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='priority',
            field=models.CharField(choices=[('default', 'default'), ('normal', 'normal'), ('high', 'high')], default='default', max_length=10),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='sound',
            field=models.CharField(choices=[('default', 'default'), ('null', None)], default='default', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='subtitle',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='thumb_image',
            field=models.ImageField(blank=True, null=True, upload_to='notification/%Y/%m'),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usernotification',
            name='ttl',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usernotification',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usernotification',
            name='notification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='notification.PushNotification'),
        ),
    ]

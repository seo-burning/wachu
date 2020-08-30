# Generated by Django 3.0.9 on 2020-08-30 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0009_usernotification_push_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='pushnotification',
            name='params',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='pushnotification',
            name='route',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='params',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='route',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

# Generated by Django 2.2.3 on 2019-08-06 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_notice_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'female'), ('male', 'male')], max_length=100, null=True),
        ),
    ]

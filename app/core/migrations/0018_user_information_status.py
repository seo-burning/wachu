# Generated by Django 3.0.6 on 2020-07-16 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20200715_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='information_status',
            field=models.CharField(choices=[('basic', 'basic'), ('pick', 'pick'), ('done', 'done'), ('pass', 'pass')], default='basic', max_length=100),
        ),
    ]

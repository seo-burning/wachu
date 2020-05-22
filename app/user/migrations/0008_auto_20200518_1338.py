# Generated by Django 3.0.6 on 2020-05-18 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_recipient_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipient',
            options={'ordering': ['primary']},
        ),
        migrations.AddField(
            model_name='recipient',
            name='primary',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 3.0.8 on 2020-07-25 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_user_view_stores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

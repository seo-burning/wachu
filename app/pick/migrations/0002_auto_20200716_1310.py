# Generated by Django 3.0.6 on 2020-07-16 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pick', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickabresult',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='pickAB_results', to=settings.AUTH_USER_MODEL),
        ),
    ]
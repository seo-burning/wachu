# Generated by Django 2.2.6 on 2020-04-01 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20191001_0632'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=250, null=True)),
                ('contact_number', models.CharField(max_length=250, null=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_address_set', to='store.Store')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

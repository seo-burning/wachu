# Generated by Django 3.0.6 on 2020-06-25 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PreorderCampaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('ordering', models.IntegerField(default=999)),
                ('name', models.CharField(max_length=255)),
                ('display_name', models.CharField(default='Need to tranlate', max_length=255)),
                ('view', models.PositiveIntegerField(default=0)),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('estimated_delivery_date', models.DateField()),
                ('cover_picture', models.ImageField(blank=True, upload_to='pre-order/%Y/%m')),
                ('list_thumb_picture', models.ImageField(blank=True, upload_to='pre-order/%Y/%m')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

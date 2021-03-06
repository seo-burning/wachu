# Generated by Django 2.2.3 on 2019-09-02 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0005_auto_20190828_0645'),
    ]

    operations = [
        migrations.CreateModel(
            name='MagazinePublish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('date', models.DateField(verbose_name='Published Date')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='postgroup',
            name='published_magazine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='publish.MagazinePublish'),
        ),
    ]

# Generated by Django 2.2.6 on 2020-04-04 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_storeaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('review', models.CharField(max_length=500, null=True)),
                ('contact_number', models.CharField(max_length=250, null=True)),
                ('rating', models.IntegerField()),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_review_set', to='store.Store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='StoreSurvey',
        ),
    ]

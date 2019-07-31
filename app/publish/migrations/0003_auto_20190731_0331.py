# Generated by Django 2.2.3 on 2019-07-31 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0002_auto_20190705_0945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainpagepublish',
            name='main_section_post_group_list',
        ),
        migrations.RemoveField(
            model_name='mainpagepublish',
            name='top_section_post_group',
        ),
        migrations.AddField(
            model_name='postgroup',
            name='published_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='publish.MainPagePublish'),
        ),
    ]

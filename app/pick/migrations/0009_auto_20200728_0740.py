# Generated by Django 3.0.8 on 2020-07-28 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0008_auto_20200726_1101'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pickabresult',
            options={'ordering': ['-created_at'], 'verbose_name': 'Pick AB Results / AB 픽 결과', 'verbose_name_plural': 'Pick AB Results / AB 픽 결과'},
        ),
    ]

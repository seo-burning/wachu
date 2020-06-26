# Generated by Django 3.0.6 on 2020-06-25 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('preorder', '0001_initial'),
        ('product', '0079_auto_20200625_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_preorder',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='preorder_campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='preorder.PreorderCampaign'),
        ),
    ]

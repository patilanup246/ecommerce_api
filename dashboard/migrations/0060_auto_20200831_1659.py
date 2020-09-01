# Generated by Django 2.2 on 2020-08-31 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0059_auto_20200831_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default='pnbmd', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='ordertrackstatus',
            name='orderTrackStatus_id',
            field=models.CharField(blank=True, default='dwegf', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(blank=True, default='OTKES', max_length=100, unique=True),
        ),
    ]
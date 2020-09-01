# Generated by Django 2.2 on 2020-08-24 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0054_auto_20200822_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_subscribe',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default='uvpsk', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(blank=True, default='EOAUS', max_length=100, unique=True),
        ),
    ]
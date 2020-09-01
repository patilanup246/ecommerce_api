# Generated by Django 2.2 on 2020-07-31 10:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_auto_20200730_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='offer',
            name='promo_code',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default='runrg', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(blank=True, default='uqtsr', max_length=100, unique=True),
        ),
    ]
# Generated by Django 2.2 on 2020-08-05 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0031_auto_20200805_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default='fbfjl', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(blank=True, default='lnoaw', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product_category',
            name='product_thumbnail',
            field=models.FileField(blank=True, null=True, upload_to='productCategoryImages/'),
        ),
    ]
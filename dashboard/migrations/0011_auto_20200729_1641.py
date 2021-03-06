# Generated by Django 2.2 on 2020-07-29 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0010_auto_20200729_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default='jvwvi', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(blank=True, default='elxnv', max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Shipping_address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('loc_latitude', models.FloatField(blank=True, null=True)),
                ('loc_lonitude', models.FloatField(blank=True, null=True)),
                ('address1', models.CharField(blank=True, max_length=500, null=True)),
                ('address2', models.CharField(blank=True, max_length=500, null=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('address_category', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_dashboard_shipping_address_related', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.RegisterUser')),
                ('write_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_dashboard_shipping_address_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

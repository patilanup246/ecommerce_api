# Generated by Django 2.2 on 2020-08-01 08:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0022_auto_20200801_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default='qjzbo', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(blank=True, default='ogokk', max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Delivery_boy_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(max_length=500, null=True, validators=[django.core.validators.RegexValidator(message="Email Id must be entered in the format: example326@gmail.com' Up to 50 character allowed.", regex='^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$')])),
                ('mob_no', models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '999999999',0989279999 Up to 14 digits allowed.", regex='^(\\+91[\\-\\s]?)?[0]?(91)?[789]\\d{9}$')])),
                ('OTP', models.IntegerField(blank=True, null=True)),
                ('image', models.CharField(blank=True, max_length=500, null=True)),
                ('address1', models.CharField(blank=True, max_length=500, null=True)),
                ('address2', models.CharField(blank=True, max_length=500, null=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('id_proof_photo', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_dashboard_delivery_boy_data_related', to=settings.AUTH_USER_MODEL)),
                ('write_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_dashboard_delivery_boy_data_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

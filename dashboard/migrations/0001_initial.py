# Generated by Django 2.2 on 2020-07-27 05:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('order_id', models.CharField(blank=True, default='zegbq', max_length=100, unique=True)),
                ('delivery_boy_id', models.IntegerField(blank=True, null=True)),
                ('order_value', models.FloatField(blank=True, null=True)),
                ('offer_Id', models.IntegerField(blank=True, null=True)),
                ('discount', models.FloatField(blank=True, null=True)),
                ('wallet_amount', models.FloatField(blank=True, null=True)),
                ('payable_amount', models.FloatField(blank=True, null=True)),
                ('payment_status', models.BooleanField(blank=True, default=False, null=True)),
                ('payment_mode', models.CharField(blank=True, choices=[('wallet', 'wallet'), ('cod', 'cod'), ('debit_card', 'debit_card'), ('credit_card', 'credit_card')], max_length=20, null=True)),
                ('order_status', models.CharField(blank=True, choices=[('pending', 'pending'), ('in_transit', 'in_transit'), ('delivered', 'delivered')], default='pending', max_length=20, null=True)),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_dashboard_order_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegisterUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('userId', models.IntegerField(blank=True, null=True)),
                ('userName', models.CharField(blank=True, max_length=20, null=True)),
                ('first_name', models.CharField(blank=True, max_length=35, null=True)),
                ('last_name', models.CharField(blank=True, max_length=35, null=True)),
                ('image', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(max_length=50, null=True, validators=[django.core.validators.RegexValidator(message="Email Id must be entered in the format: example326@gmail.com' Up to 50 character allowed.", regex='^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$')])),
                ('password', models.CharField(blank=True, max_length=20, null=True)),
                ('mob_no', models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '999999999',0989279999 Up to 14 digits allowed.", regex='^(\\+91[\\-\\s]?)?[0]?(91)?[789]\\d{9}$')])),
                ('OTP', models.IntegerField(blank=True, null=True)),
                ('fb_check', models.CharField(blank=True, max_length=20, null=True)),
                ('loc_latitude', models.FloatField(blank=True, null=True)),
                ('loc_lonitude', models.FloatField(blank=True, null=True)),
                ('address1', models.CharField(blank=True, max_length=30, null=True)),
                ('address2', models.CharField(blank=True, max_length=30, null=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('subscribe', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=False)),
                ('wallet_amount', models.FloatField(blank=True, null=True)),
                ('payment_mode', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_dashboard_registeruser_related', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('write_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_dashboard_registeruser_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('category_id', models.IntegerField(blank=True)),
                ('category_name', models.CharField(blank=True, max_length=200)),
                ('category_description', models.CharField(blank=True, max_length=200, null=True)),
                ('product_thumbnail', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_dashboard_product_category_related', to=settings.AUTH_USER_MODEL)),
                ('write_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_dashboard_product_category_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('product_id', models.CharField(blank=True, default='ocmzd', max_length=100, unique=True)),
                ('product_name', models.CharField(blank=True, max_length=200)),
                ('product_description', models.CharField(max_length=200)),
                ('product_images', models.FileField(blank=True, db_column='product_images', null=True, upload_to='productImages/')),
                ('product_price', models.FloatField(null=True)),
                ('product_status', models.CharField(max_length=200)),
                ('discount', models.FloatField(null=True)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_dashboard_product_related', to=settings.AUTH_USER_MODEL)),
                ('product_category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Product_category')),
                ('write_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_dashboard_product_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order_Product_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_dashboard_order_product_list_related', to=settings.AUTH_USER_MODEL)),
                ('order_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Order')),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Product')),
                ('write_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_dashboard_order_product_list_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.RegisterUser'),
        ),
        migrations.AddField(
            model_name='order',
            name='write_user',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_dashboard_order_related', to=settings.AUTH_USER_MODEL),
        ),
    ]

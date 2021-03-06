# Generated by Django 2.2 on 2020-08-12 09:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0042_auto_20200807_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default='smdzu', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(blank=True, default='SBWCX', max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('write_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, null=True)),
                ('phone', models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '999999999',0989279999 Up to 14 digits allowed.", regex='^(\\+91[\\-\\s]?)?[0]?(91)?[789]\\d{9}$')])),
                ('otp', models.CharField(blank=True, max_length=9, null=True)),
                ('count', models.IntegerField(default=0, help_text='Number of opt_sent')),
                ('create_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_dashboard_phoneotp_related', to=settings.AUTH_USER_MODEL)),
                ('write_user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='written_by_dashboard_phoneotp_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

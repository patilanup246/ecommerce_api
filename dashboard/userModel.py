from django.contrib.auth.models import User
from django.db import models
from .models import BaseModel
from django.core.validators import RegexValidator
import datetime


class RegisterUser(BaseModel):
    phone_regex = RegexValidator(regex=r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$',
                                 message="Phone number must be entered in the format: '999999999',0989279999 Up to 14 digits allowed.")
    email_regex = RegexValidator(regex=r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
                                 message="Email Id must be entered in the format: example326@gmail.com' Up to 50 character allowed.")  #^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  for custom

    userId = models.IntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    userName = models.CharField(max_length=500, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    image = models.FileField(blank=True, null=True, upload_to='UserProfileImages/')

    email = models.CharField(validators=[email_regex], max_length=500, null=True, blank=True)
    password = models.CharField(max_length=20, null=True, blank=True)
    mob_no = models.CharField(validators=[phone_regex], max_length=15, null=True, blank=True)

    OTP = models.IntegerField(null=True, blank=True)
    fb_check = models.CharField(max_length=500, null=True, blank=True)
    loc_latitude = models.FloatField(null=True, blank=True)
    loc_lonitude = models.FloatField(null=True, blank=True)
    address1 = models.CharField(max_length=500, null=True, blank=True)
    address2 = models.CharField(max_length=500, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)

    subscribe = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    wallet_amount = models.FloatField(null=True, blank=True, default=0.0)

    payment_mode_choices = (
        ('wallet', 'wallet'),
        ('cod', 'cod'),
        ('debit_card', 'debit_card'),
        ('credit_card', 'credit_card'),
    )

    payment_mode = models.CharField(null=True, blank=True, max_length=20, choices=payment_mode_choices)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def user_images_URL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.pk is None:
            self.created_at = datetime.datetime.now()
            # usr_name = self.userName
            print("in save method")
            print(self.mob_no)
            print(self.email)
            if self.email is not None:
                usr_name = self.email
            else:
                usr_name = self.mob_no
            # usr_name = self.mob_no
            print(usr_name)
            # user_obj = User.objects.create_user(
            #     username=usr_name, password=self.password, is_staff=False, email=self.email,
            #     first_name=self.first_name, last_name=self.last_name
            # )
            user_obj = User.objects.create_user(
                username=usr_name, password=self.password, is_staff=False
            )
            user_data = list(User.objects.filter(username=user_obj).values('pk'))
            user_data[0].get('pk')
            print(user_data[0].get('pk'))
            self.userId = user_data[0].get('pk')
            self.user_id = user_data[0].get('pk')
            res = super(RegisterUser, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            res = super(RegisterUser, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        return res


class PhoneOTP(BaseModel):
    phone_regexForOtp = RegexValidator(regex=r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$',
                                 message="Phone number must be entered in the format: '999999999',0989279999 Up to 14 digits allowed.")

    phone = models.CharField(validators=[phone_regexForOtp], max_length=15, null=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of opt_sent')
    validated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)

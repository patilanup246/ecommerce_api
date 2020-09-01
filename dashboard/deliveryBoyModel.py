from .models import BaseModel
from django.db import models
import datetime
from django.core.validators import RegexValidator

class Delivery_boy_data(BaseModel):
    phone_regex = RegexValidator(regex=r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$',
                                 message="Phone number must be entered in the format: '999999999',0989279999 Up to 14 digits allowed.")
    email_regex = RegexValidator(regex=r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
                                 message="Email Id must be entered in the format: example326@gmail.com' Up to 50 character allowed.")

    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(validators=[email_regex], max_length=500, null=True)
    mob_no = models.CharField(validators=[phone_regex], max_length=15, null=True)
    OTP = models.IntegerField(null=True, blank=True)
    image = models.CharField(max_length=500, null=True, blank=True)
    address1 = models.CharField(max_length=500, null=True, blank=True)
    address2 = models.CharField(max_length=500, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    id_proof_photo = models.CharField(max_length=500, null=True, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.pk is None:
            self.created_at = datetime.datetime.now()
            # usr_name = self.userName
            # print(usr_name)
            # user_obj = User.objects.create_user(
            #     username=usr_name, password=self.password, is_staff=False, email=self.email,
            #     first_name=self.first_name, last_name=self.last_name
            # )
            # user_data = list(User.objects.filter(username=user_obj).values('pk'))
            # user_data[0].get('pk')
            # print(user_data[0].get('pk'))
            # self.userId = user_data[0].get('pk')
            # self.user_id = user_data[0].get('pk')
            res = super(Delivery_boy_data, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            res = super(Delivery_boy_data, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        return res
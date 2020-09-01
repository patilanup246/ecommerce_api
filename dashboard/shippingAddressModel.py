from django.db import models
from .models import BaseModel
from .userModel import RegisterUser
import datetime

class Shipping_address(BaseModel):
    user_id = models.ForeignKey(RegisterUser, on_delete=models.SET_NULL, null=True, blank=True)
    loc_latitude = models.FloatField(null=True, blank=True)
    loc_lonitude = models.FloatField(null=True, blank=True)
    address1 = models.CharField(max_length=500, null=True, blank=False)
    address2 = models.CharField(max_length=500, null=True, blank=False)
    pincode = models.IntegerField(null=True, blank=False)
    address_category = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.pk is None:
            self.created_at = datetime.datetime.now()

            res = super(Shipping_address, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            res = super(Shipping_address, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        return res
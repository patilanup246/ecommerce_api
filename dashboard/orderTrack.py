from .models import BaseModel
from django.db import models
from django.utils import timezone
import datetime
import random, string
from .orderModel import Order
from .userModel import RegisterUser
from .deliveryBoyModel import Delivery_boy_data
from .vendorStockModel import Vendor_Stock

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

class OrderTrackStatus(BaseModel):
    orderTrackStatus_id = models.CharField(default=randomword(5), null=False, blank=True, max_length=100, unique=True)
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.ForeignKey(RegisterUser, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_boy_id = models.ForeignKey(Delivery_boy_data, on_delete=models.SET_NULL, null=True, blank=True)
    stored_id = models.ForeignKey(Vendor_Stock, on_delete=models.SET_NULL, null=True, blank=True)
    user_lat = models.FloatField(null=True, blank=True)
    user_lon = models.FloatField(null=True, blank=True)
    delivery_lat = models.FloatField(null=True, blank=True)
    delivery_lon = models.FloatField(null=True, blank=True)
    order_Status = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.pk is None:
            self.created_at = datetime.datetime.now()
            self.orderTrackStatus_id = randomword(5)
            res = super(OrderTrackStatus, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        else:
            self.orderTrackStatus_id = randomword(5)
            self.updated_at = datetime.datetime.now()
            res = super(OrderTrackStatus, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        return res

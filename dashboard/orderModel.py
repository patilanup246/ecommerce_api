from .models import BaseModel
from django.db import models
from .userModel import RegisterUser
# import datetime
from django.utils import timezone
import random, string
from .productModel import Product, Product_category
from .offerModel import Offer


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

class Order(BaseModel):
    order_id = models.CharField(default=randomword(5), null=False, blank=True, max_length=100, unique=True)
    user_id = models.ForeignKey(RegisterUser, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_boy_id = models.IntegerField(null=True, blank=True)
    order_value = models.FloatField(null=True, blank=True)
    # offer_Id = models.IntegerField(null=True, blank=True)
    offer_Id = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.FloatField(null=True, blank=True, default=0.0)
    wallet_amount = models.FloatField(null=True, blank=True)
    payable_amount = models.FloatField(null=True, blank=True)
    payment_status = models.BooleanField(null=True, blank=True, default=False)
    # payment_mode = models.CharField(null=True, blank=True, max_length=100)

    payment_mode_choices = (
        ('wallet', 'wallet'),
        ('cod', 'cod'),
        ('debit_card', 'debit_card'),
        ('credit_card', 'credit_card'),
    )

    payment_mode = models.CharField(null=True, blank=True, max_length=20, choices=payment_mode_choices)

    order_status_choices = (
        ('pending', 'pending'),
        ('in_transit', 'in_transit'),
        ('delivered', 'delivered'),
    )

    order_status = models.CharField(null=True, blank=True, max_length=20, choices=order_status_choices, default='pending')
    # order_status = models.CharField(null=True, blank=True, max_length=100)
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    # additional fields or parameters are added , according to the requirements from mobile end
    subTotal = models.FloatField(null=True, blank=True, default=0.0)
    deliveryCharges = models.FloatField(null=True, blank=True, default=0.0)
    taxCharges = models.FloatField(null=True, blank=True, default=0.0)
    discountCouponCode = models.CharField(null=True, blank=True, max_length=100)
    grandTotal = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return self.order_id

    #
    # @property
    # def get_cart_total_discount(self):
    #     orderitems = self.order_product_list_set.all()
    #     total = round(sum([item.get_total_discount for item in orderitems]), 2)
    #     # print(total)
    #     return total

    @property
    def get_cart_total_discount(self):
        orderitems = self.order_product_list_set.all()
        total = round(sum([item.get_total for item in orderitems]), 2)
        if self.offer_Id is not None:
            discount = round((total * (self.offer_Id.discount / 100)), 2)
            # totalPrice = total - discount
            # return totalPrice
            return discount
        else:
            # print(total)
            return 0.0

    @property
    def get_cart_total_GST(self):
        orderitems = self.order_product_list_set.all()
        total = round(sum([item.get_total for item in orderitems]), 2)
        totalGst = round((total * (18/100)), 2)
        return totalGst

    @property
    def get_cart_sub_total(self):
        print("ok in gst")
        orderitems = self.order_product_list_set.all()
        total = round(sum([item.get_total for item in orderitems]), 2)
        totalGst = round((total * (18 / 100)), 2)
        # print(total)

        if self.offer_Id is not None:
            print("in in offer id")
            discount = round((total * (self.offer_Id.discount / 100)), 2)
            subTotal = total + totalGst - discount
            print(subTotal)
            return subTotal
        else:
            subTotal = total + totalGst
            print(subTotal)
            return subTotal

    @property
    def get_cart_total(self):
        orderitems = self.order_product_list_set.all()
        total = round(sum([item.get_total for item in orderitems]), 2)
        return total

    @property
    def get_cart_quantities(self):
        orderitems = self.order_product_list_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.order_product_list_set.all().count()
        # total = sum([item.quantity for item in orderitems])
        total = orderitems
        return total

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            # self.created_at = datetime.datetime.now()
            self.created_at = timezone.now()
            self.order_id = randomword(5)
            order_save = super(Order, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        else:
            # self.updated_at = datetime.datetime.now()
            self.updated_at = timezone.now()
            self.order_id = randomword(5)
            order_save = super(Order, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        return order_save

class Order_Product_List(BaseModel):
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_price = models.FloatField(null=True, blank=True)
    # offer_Id = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True) # this field is added by me
    quantity = models.IntegerField(default=0,null=True, blank=True)
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return str(self.id)
    # this for perticular product discount
    # @property
    # def get_total(self):
    #     total = round((self.product_id.product_price * self.quantity),2)
    #     if self.offer_Id is not None:
    #         discount = round((total * (self.offer_Id.discount / 100)), 2)
    #         totalPrice = total - discount
    #         return totalPrice
    #     else:
    #         print(total)
    #         return total

    # @property
    # def get_total_discount(self):
    #
    #     if self.offer_Id is not None:
    #         total = round((self.product_id.product_price * self.quantity),2)
    #         discount = round((total * (self.offer_Id.discount / 100)),2)
    #         return discount
    #     else:
    #         return 0.0

    @property
    def get_total(self):
        total = round((self.product_id.product_price * self.quantity),2)
        return total


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            # self.created_at = datetime.datetime.now()
            self.created_at = timezone.now()
            order_Product_List_save = super(Order_Product_List, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        else:
            # self.updated_at = datetime.datetime.now()
            self.updated_at = timezone.now()
            order_Product_List_save = super(Order_Product_List, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        return order_Product_List_save




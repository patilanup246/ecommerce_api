from .models import BaseModel
from django.db import models
import datetime
import random, string
from .userModel import RegisterUser


def randomword(length):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))

def randomNo():
    return random.randint(1000,9999)

class Product_category(BaseModel):
    category_id = models.IntegerField(null=False, blank=True, default=randomNo)
    category_name = models.CharField(null=False, blank=True, max_length=200)
    category_description = models.CharField(null=True, blank=True, max_length=200)
    # product_thumbnail = models.CharField(null=True, blank=True, max_length=200)
    product_thumbnail = models.FileField(blank=True, null=True, upload_to='productCategoryImages/')
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.category_name

    @property
    def products(self):
        return self.product_set.all()

    @property
    def product_thumbnail_URL(self):
        try:
            url = self.product_thumbnail.url
        except:
            url = ''
        return url


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            self.created_at = datetime.datetime.now()
            product_category_save = super(Product_category, self).save(force_insert=False, force_update=False,
                                                                       using=None,
                                                                       update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            product_category_save = super(Product_category, self).save(force_insert=False, force_update=False,
                                                                       using=None,
                                                                       update_fields=None)
        return product_category_save


class Product(BaseModel):
    product_id = models.CharField(default=randomword(5), null=False, blank=True, max_length=100, unique=True)
    product_category_id = models.ForeignKey(Product_category, on_delete=models.SET_NULL, null=True, blank=True) # models.CASCADE
    product_name = models.CharField(null=False, blank=True, max_length=200)
    product_description = models.CharField(null=False, blank=False, max_length=200)
    # product_images = models.CharField(null=False, blank=False, max_length=200)
    product_images = models.FileField(db_column='product_images', blank=True, null=True, upload_to='productImages/')
    # product_images = models.ImageField(blank=True, null=True, upload_to='productImages/')
    product_price = models.FloatField(null=True)
    # product_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, null=True)
    product_status = models.CharField(null=False, blank=False, max_length=200)
    discount = models.FloatField(null=True, blank=True)
    # discount = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    # product_Subscribe = models.ForeignKey(Product_Subscribe, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def product_images_URL(self):
        try:
            url = self.product_images.url
        except:
            url = ''
        return url

    # @property
    # def get_quantityt(self):
    #     print("get product quantity")
    #     vendor_Stock = self.vendor_stock_set.all()
    #     # total = round(sum([item.quantity for item in vendor_Stock]), 2)
    #     # print(total)
    #     print(vendor_Stock)
    #     print(self.id.vendor_Stock)
    #     return 0.0


    def __str__(self):
        return self.product_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            self.product_id = randomword(5)
            self.created_at = datetime.datetime.now()
            product_save = super(Product, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            product_save = super(Product, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        return product_save


class Product_Subscribe(BaseModel):
    user_id = models.ForeignKey(RegisterUser, on_delete=models.SET_NULL, null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    # subscription_price = models.FloatField(null=True)

    schedule_type_choices = (
        ('Daily', 'Daily'),
        ('Alternate Day', 'Alternate Day'),
        ('Every 3 days', 'Every 3 days'),
        ('Weekly', 'Weekly'),
    )

    schedule_type = models.CharField(null=True, blank=True, max_length=30, choices=schedule_type_choices)
    # subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_start_date = models.DateField(null=True, blank=True)
    # subscription_end_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)

    delete_subscription_reason_choices = (
        # ('Quality issue', 'Quality issue'),
        ('Delivery is always late', 'Delivery is always late'),
        ('Bill issue', 'Bill issue'),
        ('Changing product', 'Changing product'),
        ('Moving out of society', 'Moving out of society'),
        ('Irregular deliveries', 'Irregular deliveries'),
        ('Bag not received', 'Bag not received'),
        ('Issue with customer care', 'Issue with customer care'),
        ('Other', 'Other'),
    )

    delete_subscription_reason = models.CharField(null=True, blank=True, max_length=100, choices=delete_subscription_reason_choices)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return str(self.id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:

            self.created_at = datetime.datetime.now()
            product_Subscribe_save = super(Product_Subscribe, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            product_Subscribe_save = super(Product_Subscribe, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        return product_Subscribe_save


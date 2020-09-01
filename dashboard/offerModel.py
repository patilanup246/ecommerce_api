from .models import BaseModel
from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

class Offer(BaseModel):
    # offer_id = models.IntegerField(null=True, blank=True,)
    offer_start_date = models.DateTimeField(null=True, blank=True)
    offer_end_date = models.DateTimeField(null=True, blank=True)
    offer_title_name = models.CharField(null=True, blank=True, max_length=200)
    offers_on_product = models.IntegerField(null=True, blank=True)
    offer_post = models.CharField(null=True, blank=True, max_length=800)
    offer_description = models.CharField(null=True, blank=True, max_length=1000)
    promo_code = models.CharField(null=True, blank=True, max_length=100, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0, null=True, blank=True)
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:

            self.created_at = datetime.datetime.now()
            offer = super(Offer, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            offer = super(Offer, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        return offer

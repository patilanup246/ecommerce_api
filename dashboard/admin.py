from django.contrib import admin
from .productModel import Product_category, Product, Product_Subscribe
from .orderModel import Order, Order_Product_List
from .userModel import RegisterUser, PhoneOTP
from .shippingAddressModel import Shipping_address
from .offerModel import Offer
from .deliveryBoyModel import Delivery_boy_data
from .vendorModel import Vendor_management
from .vendorStockModel import Vendor_Stock
from .orderTrack import OrderTrackStatus

# admin.site.register(admin)
admin.site.register(RegisterUser)
admin.site.register(Product)
admin.site.register(Product_category)
admin.site.register(Product_Subscribe)
admin.site.register(Order)
admin.site.register(Order_Product_List)
admin.site.register(Shipping_address)
admin.site.register(Offer)
admin.site.register(Delivery_boy_data)
admin.site.register(Vendor_management)
admin.site.register(Vendor_Stock)
admin.site.register(PhoneOTP)
admin.site.register(OrderTrackStatus)


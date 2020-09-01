from allauth import exceptions
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dashboard.productModel import Product, Product_category, Product_Subscribe
from dashboard.orderModel import Order, Order_Product_List
from dashboard.userModel import RegisterUser
from dashboard.shippingAddressModel import Shipping_address
from dashboard.offerModel import Offer
from dashboard.deliveryBoyModel import Delivery_boy_data
from dashboard.vendorModel import Vendor_management
from dashboard.vendorStockModel import Vendor_Stock
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.core.validators import RegexValidator
import re


class UserRegisterSerializer(serializers.ModelSerializer):
    # userName = serializers.CharField(label='Username')
    # first_name = serializers.CharField(label='first_name')
    # last_name = serializers.CharField(label='last_name')
    # email2 = serializers.EmailField(label='Confirm Email')
    # email = serializers.EmailField(label='Email Address')
    full_name = serializers.CharField(label='Full Name')
    mob_no = serializers.CharField(label='Mobile_No')
    password = serializers.CharField(label='Password')
    # password2 = serializers.CharField(label='Confirm Password')

    def validate_password(self, value):
        data = self.get_initial()
        password1 = data.get("password")
        print(value)
        # password2 = value
        # if password1 != password2:
        #     raise serializers.ValidationError("Password Must Match")

        """Validates that a password is as least 6 characters long and has at least
            2 digits and 1 Upper case letter.
            """
        msg = 'Note: password is as least 6 characters long and has at least 2 digits and 1 Upper case letter'
        min_length = 6

        if len(value) < min_length:
            raise serializers.ValidationError('Password must be at least {0} characters '
                                              'long.'.format(min_length) + msg)

        # # check for 2 digits
        # if sum(c.isdigit() for c in value) < 2:
        #     raise serializers.ValidationError('Password must container at least 2 digits.' + msg)
        #
        # # check for uppercase letter
        # if not any(c.isupper() for c in value):
        #     raise serializers.ValidationError('Password must container at least 1 uppercase letter.' + msg)

        return value

    # def validate_email(self, value):
    #     data = self.get_initial()
    #     email = data.get("email")
    #     regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    #     if (re.search(regex, email)):
    #         username_qs = User.objects.filter(username=email)
    #         if username_qs.exists():
    #             raise serializers.ValidationError("Email Id already exists")
    #         else:
    #             pass
    #         return value
    #     raise serializers.ValidationError("invalid Email id")

    def validate_mob_no(self, value):
        data = self.get_initial()
        mob_no = data.get("mob_no")
        regex = '^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$'
        if (re.search(regex, mob_no)):

            username_qs = User.objects.filter(username=mob_no)
            registerUser = RegisterUser.objects.filter(mob_no=mob_no)
            if username_qs.exists() and registerUser.exists():
                raise serializers.ValidationError("mob_no already exists")
            else:
                pass
            return value
        else:
            raise serializers.ValidationError(
                    "Phone number must be entered in the format: '9999999999',9892799999 Up to 14 digits allowed.")


    def create(self, validated_data):

        user = RegisterUser.objects.create(
            # userName=validated_data['email'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name'],
            # email=validated_data['email'],
            mob_no=validated_data['mob_no'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        # user.set_password(validated_data['mob_no'])
        # user.mob_no = validated_data['mob_no']
        #
        # user.save()

        return validated_data

    class Meta:
        model = RegisterUser
        fields = ('full_name', 'mob_no', 'password')


class SuperUserRegisterSerializer(serializers.ModelSerializer):
    # userName = serializers.CharField(label='Username')
    first_name = serializers.CharField(label='first_name')
    last_name = serializers.CharField(label='last_name')
    # email2 = serializers.EmailField(label='Confirm Email')
    email = serializers.EmailField(label='Email Address')
    mob_no = serializers.CharField(label='Mobile_No')

    password = serializers.CharField(label='Password')
    password2 = serializers.CharField(label='Confirm Password')

    def validate_password2(self, value):
        data = self.get_initial()
        password1 = data.get("password")
        password2 = value
        if password1 != password2:
            raise serializers.ValidationError("Password Must Match")

        """Validates that a password is as least 8 characters long and has at least
            2 digits and 1 Upper case letter.
            """
        msg = 'Note: password is as least 8 characters long and has at least 2 digits and 1 Upper case letter'
        min_length = 8

        if len(value) < min_length:
            raise serializers.ValidationError('Password must be at least {0} characters '
                                              'long.'.format(min_length) + msg)

        # check for 2 digits
        if sum(c.isdigit() for c in value) < 2:
            raise serializers.ValidationError('Password must container at least 2 digits.' + msg)

        # check for uppercase letter
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError('Password must container at least 1 uppercase letter.' + msg)

        return value

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get("email")
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (re.search(regex, email)):
            username_qs = User.objects.filter(username=email)
            if username_qs.exists():
                raise serializers.ValidationError("Email Id already exists")
            else:
                pass
            return value
        raise serializers.ValidationError("invalid Email id")

    def validate_mob_no(self, value):
        data = self.get_initial()
        mob_no = data.get("mob_no")
        regex = '^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$'
        if (re.search(regex, mob_no)):
            return value
        else:
            raise serializers.ValidationError(
                "Phone number must be entered in the format: '9999999999',9892799999 Up to 14 digits allowed.")

    # def validate_userName(self, value):
    #     data = self.get_initial()
    #     userName = data.get("userName")
    #     # username_qs = User.objects.filter(username=userName)
    #     # registerUser = RegisterUser.objects.filter(userName=userName, user=username_qs)
    #     min_length = 5
    #     if len(value) < min_length:
    #         raise serializers.ValidationError('Username must be at least {0} characters '
    #                                 'long.'.format(min_length))
    #
    #     max_length = 20
    #     if len(value) > max_length:
    #         raise serializers.ValidationError('Username not more {0} characters '
    #                                           'long.'.format(max_length))
    #
    #     username_qs = User.objects.filter(username=userName)
    #     if username_qs.exists():
    #        raise serializers.ValidationError("Username already exists")
    #     else:
    #         pass
    #
    #     return value

    def create(self, validated_data):

        # registerUser = RegisterUser.objects.create(
        #     userName=validated_data['email'],
        #     first_name=validated_data['first_name'],
        #     last_name=validated_data['last_name'],
        #     email=validated_data['email'],
        #     mob_no=validated_data['mob_no'],
        #     password=validated_data['password']
        # )
        superuser = User.objects.create_user(
                username=validated_data['email'], password=validated_data['password']
            )
        user = User.objects.get(username=validated_data['email'])
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()

        return validated_data

    class Meta:
        model = RegisterUser
        fields = ('first_name', 'last_name', 'email', 'mob_no', 'password', 'password2')  # 'userName',


# for create product through api
class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = ['id', 'product_id', 'product_category_id', 'product_name', 'product_description', 'product_images',
                  'product_price', 'product_status', 'discount', 'rating', 'status']
        read_only_fields = ('product_category_id',)
        # depth = 1


# for create productCategory through api
class ProductCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Product_category
        fields = ['id', 'category_id', 'category_name', 'category_description', 'product_thumbnail', 'status',
                  'products']

    def create(self, validated_data):
        products = validated_data.pop('products')
        product_category = Product_category.objects.create(**validated_data)
        for productDetail in products:
            print(productDetail)
            Product.objects.create(product_category_id=product_category, **productDetail)
        return product_category

    def update(self, instance, validated_data):
        products = validated_data.pop('products')
        print(products)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.category_description = validated_data.get('category_description', instance.category_description)
        instance.product_thumbnail = validated_data.get('product_thumbnail', instance.product_thumbnail)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        keep_products = []
        # existing_ids = [c.id for c in instance.products]
        for product in products:
            if 'id' in product.keys():
                if Product.objects.filter(id=product['id']).exists():
                    c = Product.objects.get(id=product['id'])
                    c.product_id = product.get('product_id', c.product_id)
                    c.product_category_id = product.get('product_category_id', c.product_category_id)
                    c.product_name = product.get('product_name', c.product_name)
                    c.product_description = product.get('product_description', c.product_description)
                    c.product_images = product.get('product_images', c.product_images)
                    c.product_price = product.get('product_price', c.product_price)
                    c.product_status = product.get('product_status', c.product_status)
                    c.discount = product.get('discount', c.discount)
                    c.rating = product.get('rating', c.rating)
                    c.status = product.get('status', c.status)
                    c.save()
                    keep_products.append(c.id)
                else:
                    continue
            else:
                Product.objects.create(product_category_id=instance, **product)
                keep_products.append(c.id)

        for product in instance.products:
            if product.id not in keep_products:
                product.delete()

        return instance


# get product Category through api
class GetProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_category
        exclude = ['create_date', 'write_date', 'create_user', 'write_user']


# get product through api
class GetProductSerializer(serializers.ModelSerializer):
    product_category_id = GetProductCategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'product_id', 'product_name', 'product_description', 'product_images',
                  'product_price', 'product_status', 'discount', 'rating', 'status', 'product_category_id']
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    payment_mode = serializers.ChoiceField(choices=Order.payment_mode_choices, required=False)
    order_status = serializers.ChoiceField(choices=Order.order_status_choices, required=False)

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'user_id', 'delivery_boy_id', 'order_value', 'offer_Id', 'discount',
                  'wallet_amount',
                  'payable_amount', 'payment_status', 'payment_mode', 'order_status', 'status', 'created_at',
                  'updated_at', 'subTotal', 'deliveryCharges', 'taxCharges', 'discountCouponCode', 'grandTotal'
                  ]  #'get_cart_total', 'get_cart_quantities', 'get_cart_items', 'get_cart_total_discount',
                     #'get_cart_sub_total' ,'get_cart_total_GST'
        read_only_fields = ('order_id',)


class OrderproductSerializer(serializers.ModelSerializer):
    # order_id = OrderSerializer()
    product_id = ProductSerializer()

    class Meta:
        model = Order_Product_List
        fields = ['id', 'get_total', 'quantity', 'status', 'created_at', 'updated_at',
                  'product_id']
        depth = 1


class ShippingAddressSerializer(serializers.ModelSerializer):
    address1 = serializers.CharField(required=True)
    address2 = serializers.CharField(required=True)
    pincode = serializers.CharField(required=True)

    class Meta:
        model = Shipping_address
        fields = ['id', 'loc_latitude', 'loc_lonitude', 'address1', 'address2', 'pincode',
                  'address_category']  # 'order_id',
        depth = 1

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.loc_latitude = validated_data.get('loc_latitude', instance.loc_latitude)
        instance.loc_lonitude = validated_data.get('loc_lonitude', instance.loc_lonitude)
        instance.address1 = validated_data.get('address1', instance.address1)
        instance.address2 = validated_data.get('address2', instance.address2)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.address_category = validated_data.get('address_category', instance.address_category)
        instance.save()

        return instance


class OfferSerializer(serializers.ModelSerializer):
    offer_start_date = serializers.DateTimeField()
    offer_end_date = serializers.DateTimeField()

    class Meta:
        model = Offer
        fields = ['id', 'offer_start_date', 'offer_end_date', 'offer_title_name', 'offers_on_product', 'offer_post',
                  'offer_description', 'promo_code', 'status', 'created_at', 'updated_at']
        depth = 1

    def update(self, instance, validated_data):
        instance.offer_start_date = validated_data.get('offer_start_date', instance.offer_start_date)
        instance.offer_end_date = validated_data.get('offer_end_date', instance.offer_end_date)
        instance.offer_title_name = validated_data.get('offer_title_name', instance.offer_title_name)
        instance.offers_on_product = validated_data.get('offers_on_product', instance.offers_on_product)
        instance.offer_post = validated_data.get('offer_post', instance.offer_post)
        instance.offer_description = validated_data.get('offer_description', instance.offer_description)
        instance.promo_code = validated_data.get('promo_code', instance.promo_code)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance


class DeliveryBoySerializer(serializers.ModelSerializer):
    # address1 = serializers.CharField(required=True)
    # address2 = serializers.CharField(required=True)
    # pincode = serializers.CharField(required=True)
    class Meta:
        model = Delivery_boy_data
        fields = ['id', 'first_name', 'last_name', 'email', 'mob_no', 'OTP', 'image', 'address1', 'address2',
                  'pincode', 'id_proof_photo', 'status']
        depth = 1

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.mob_no = validated_data.get('mob_no', instance.mob_no)
        instance.OTP = validated_data.get('OTP', instance.OTP)
        instance.image = validated_data.get('image', instance.image)
        instance.address1 = validated_data.get('address1', instance.address1)
        instance.address2 = validated_data.get('address2', instance.address2)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.id_proof_photo = validated_data.get('id_proof_photo', instance.id_proof_photo)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance


class VendorManagementSerializer(serializers.ModelSerializer):
    # userName = serializers.CharField(label='Username')
    first_name = serializers.CharField(label='first_name')
    last_name = serializers.CharField(label='last_name')
    # email2 = serializers.EmailField(label='Confirm Email')
    email = serializers.EmailField(label='Email Address')
    mob_no = serializers.CharField(label='Mobile_No')

    password = serializers.CharField(label='Password')
    password2 = serializers.CharField(label='Confirm Password')

    def validate_password2(self, value):
        data = self.get_initial()
        password1 = data.get("password")
        password2 = value
        if password1 != password2:
            raise serializers.ValidationError("Password Must Match")

        """Validates that a password is as least 8 characters long and has at least
            2 digits and 1 Upper case letter.
            """
        msg = 'Note: password is as least 8 characters long and has at least 2 digits and 1 Upper case letter'
        min_length = 8

        if len(value) < min_length:
            raise serializers.ValidationError('Password must be at least {0} characters '
                                              'long.'.format(min_length) + msg)

        # check for 2 digits
        if sum(c.isdigit() for c in value) < 2:
            raise serializers.ValidationError('Password must container at least 2 digits.' + msg)

        # check for uppercase letter
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError('Password must container at least 1 uppercase letter.' + msg)

        return value

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get("email")
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (re.search(regex, email)):
            username_qs = User.objects.filter(username=email)
            if username_qs.exists():
                raise serializers.ValidationError("Email Id already exists")
            else:
                pass
            return value
        raise serializers.ValidationError("invalid Email id")

    def validate_mob_no(self, value):
        data = self.get_initial()
        mob_no = data.get("mob_no")
        regex = '^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$'
        if (re.search(regex, mob_no)):
            return value
        else:
            raise serializers.ValidationError(
                "Phone number must be entered in the format: '9999999999',9892799999 Up to 14 digits allowed.")

    # def validate_userName(self, value):
    #     data = self.get_initial()
    #     userName = data.get("userName")
    #     # username_qs = User.objects.filter(username=userName)
    #     # registerUser = RegisterUser.objects.filter(userName=userName, user=username_qs)
    #     min_length = 5
    #     if len(value) < min_length:
    #         raise serializers.ValidationError('Username must be at least {0} characters '
    #                                 'long.'.format(min_length))
    #
    #     max_length = 20
    #     if len(value) > max_length:
    #         raise serializers.ValidationError('Username not more {0} characters '
    #                                           'long.'.format(max_length))
    #
    #     username_qs = User.objects.filter(username=userName)
    #     if username_qs.exists():
    #        raise serializers.ValidationError("Username already exists")
    #     else:
    #         pass
    #
    #     return value

    def create(self, validated_data):

        user = Vendor_management.objects.create(
            userName=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            mob_no=validated_data['mob_no'],
            password=validated_data['password']
        )
        # user.set_password(validated_data['mob_no'])
        # user.mob_no = validated_data['mob_no']
        #
        # user.save()

        return validated_data

    class Meta:
        model = Vendor_management
        fields = ('first_name', 'last_name', 'email', 'mob_no', 'password', 'password2')  # 'userName',


class GetVendorManagementSerializer(serializers.ModelSerializer):
    payment_mode = serializers.ChoiceField(choices=Vendor_management.payment_mode_choices, required=False)

    class Meta:
        model = Vendor_management
        fields = ['id', 'vendor_id', 'userName', 'login_type_id', 'first_name', 'last_name', 'email', 'password',
                  'mob_no',
                  'OTP', 'address1', 'address2', 'pincode', 'notes', 'id_proof', 'image', 'total_product_quantity',
                  'payment_status', 'payment_mode', 'stock_delivery_status', 'status', 'created_at', 'updated_at']
        depth = 1

    def update(self, instance, validated_data):
        # instance.vendor_id = validated_data.get('vendor_id', instance.vendor_id)
        # instance.userName = validated_data.get('userName', instance.userName)
        # instance.login_type_id = validated_data.get('login_type_id', instance.login_type_id)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.email = validated_data.get('email', instance.email)
        instance.address1 = validated_data.get('address1', instance.address1)
        instance.address2 = validated_data.get('address2', instance.address2)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.id_proof = validated_data.get('id_proof', instance.id_proof)
        # instance.image = validated_data.get('image', instance.image)
        instance.total_product_quantity = validated_data.get('total_product_quantity', instance.total_product_quantity)
        instance.payment_status = validated_data.get('payment_status', instance.payment_status)
        instance.payment_mode = validated_data.get('payment_mode', instance.payment_mode)
        instance.stock_delivery_status = validated_data.get('stock_delivery_status', instance.stock_delivery_status)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance


class VendorStockSerializer(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(
    #     queryset=Product.objects.all(), source='product_id', allow_null=False, required=True
    # )
    # product_category = serializers.PrimaryKeyRelatedField(
    #     queryset=Product_category.objects.all(), source='product_category_id', allow_null=False, required=True
    # )

    class Meta:
        model = Vendor_Stock
        fields = ['id', 'vendor_id', 'product_id', 'product_category_id', 'quantity', 'price', 'selling_price',
                  'status',
                  'created_at', 'updated_at']

    def update(self, instance, validated_data):
        instance.vendor_id = validated_data.get('vendor_id', instance.vendor_id)
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.product_category_id = validated_data.get('product_category_id', instance.product_category_id)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.selling_price = validated_data.get('selling_price', instance.selling_price)
        instance.status = validated_data.get('status', instance.status)

        instance.save()

        return instance


class Product_CategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True)

    class Meta:
        model = Product_category
        fields = ['id', 'category_id', 'category_name', 'category_description', 'product_thumbnail', 'status'
                  ]

    def update(self, instance, validated_data):
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.category_description = validated_data.get('category_description', instance.category_description)
        instance.product_thumbnail = validated_data.get('product_thumbnail', instance.product_thumbnail)
        instance.status = validated_data.get('status', instance.status)

        instance.save()

        return instance

class SelectProductCatrgorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Product_category
        fields = ['id', 'category_name']

class SelectProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'product_name']


class Product_viewSerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'product_id', 'product_category_id', 'product_name', 'product_description', 'product_images',
                  'product_price', 'product_status', 'discount', 'rating', 'status', 'created_at', 'updated_at'
                  ]

    def update(self, instance, validated_data):
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.product_category_id = validated_data.get('product_category_id', instance.product_category_id)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.product_description = validated_data.get('product_description', instance.product_description)
        instance.product_images = validated_data.get('product_images', instance.product_images)
        instance.product_price = validated_data.get('product_price', instance.product_price)
        instance.product_status = validated_data.get('product_status', instance.product_status)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.status = validated_data.get('status', instance.status)

        instance.save()

        return instance

class GetUserRegisterSerializer(serializers.ModelSerializer):
    payment_mode = serializers.ChoiceField(choices=RegisterUser.payment_mode_choices, required=False)

    class Meta:
        model = RegisterUser
        fields = ['id', 'userId', 'userName', 'first_name', 'last_name', 'email', 'password', 'mob_no', 'image', 'fb_check', 'loc_latitude',
                   'loc_lonitude',
                  'address1','address2', 'pincode', 'subscribe', 'status', 'wallet_amount', 'payment_mode', 'created_at', 'updated_at'
                  ]
        depth = 1

    def update(self, instance, validated_data):

        # instance.first_name = validated_data.get('first_name', instance.first_name)
        # instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.email = validated_data.get('email', instance.email)
        instance.address1 = validated_data.get('address1', instance.address1)
        instance.address2 = validated_data.get('address2', instance.address2)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.subscribe = validated_data.get('subscribe', instance.subscribe)
        instance.status = validated_data.get('status', instance.status)
        # instance.image = validated_data.get('image', instance.image)
        instance.wallet_amount = validated_data.get('wallet_amount', instance.wallet_amount)

        instance.payment_mode = validated_data.get('payment_mode', instance.payment_mode)
        instance.save()

        return instance

class Product_subscribe_serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Subscribe
        fields = ['id', 'product_id', 'schedule_type','subscription_start_date', 'subscription_end_date', 'status'
                  ]  # 'user_id',
        depth = 1

    def update(self, instance, validated_data):
        instance.schedule_type = validated_data.get('schedule_type', instance.schedule_type)
        instance.subscription_start_date = validated_data.get('subscription_start_date', instance.subscription_start_date)
        instance.subscription_end_date = validated_data.get('subscription_end_date', instance.subscription_end_date)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance
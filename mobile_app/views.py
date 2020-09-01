from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from dashboard.views import CurrentUser  # OrderHistoryView , OrderView ProductView,
from .serializers import UserRegisterSerializer, SuperUserRegisterSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework import status, viewsets
# from bson import ObjectId
from django.http import Http404
from django.contrib.auth.models import User
from dashboard.productModel import Product, Product_category, Product_Subscribe
from dashboard.orderModel import Order, Order_Product_List
from .serializers import ProductSerializer, ProductCategorySerializer, OrderproductSerializer, GetProductSerializer, \
    OrderSerializer, \
    ShippingAddressSerializer, OfferSerializer, DeliveryBoySerializer, VendorManagementSerializer, \
    GetVendorManagementSerializer, \
    VendorStockSerializer, Product_CategorySerializer, Product_viewSerializer, GetUserRegisterSerializer, \
    Product_subscribe_serializer, SelectProductCatrgorySerializer, SelectProductSerializer

import datetime
from django.db.models import (Case, CharField, Count, DateTimeField,
                              ExpressionWrapper, F, FloatField, Func, Max, Min,
                              Prefetch, Q, Sum, Value, When, Subquery)
from dashboard.userModel import RegisterUser, PhoneOTP
from dashboard.shippingAddressModel import Shipping_address
from .responseMethod import errorResponseMethodToken, successResponseMethodToken, successResponseMethod, \
    errorResponseMethod
from dashboard.offerModel import Offer
from dashboard.deliveryBoyModel import Delivery_boy_data
from dashboard.vendorModel import Vendor_management
from dashboard.vendorStockModel import Vendor_Stock
from dashboard.views import getHomePageContent, getProductByCategoryView, getOneProductDetailsView, \
    GetCurrentUserWithToken
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
import random
import re


# to get token id after login username and password
class AppToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            password = serializer.validated_data['password']
            # print(user)
            # print(password)
            token, created = Token.objects.get_or_create(user=user)
            # print("token id ")
            # print(token.user_id)
            # print(token.user)
            # print(token.user.is_staff)
            if token.user.is_staff:
                data = GetCurrentUserWithToken().get_VendorManagementData(token.user)
            else:
                data = GetCurrentUserWithToken().get_data(token.user)
            context = {"token": token.key, "userDetails": data}

            if data:
                return Response(successResponseMethodToken(request, context))  # token.key

            return Response(errorResponseMethodToken(request, 'User information not exists'))
        else:
            return Response(errorResponseMethodToken(request, serializer.errors))


# To get User Informations
class UserAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response = errorResponseMethod(request, "Credentials not provided")
        # print(request.user)
        # print(request.user.id)
        # print(request.user.is_staff)
        # print(request.user.is_superuser)
        if request.user.is_staff:
            data = CurrentUser().get_VendorManagementData(request.user)

        else:
            data = CurrentUser().get_data(request.user)
        if data:
            response = successResponseMethod(request, data)
        return Response(response)


# user register method

class CreateUserRegister(CreateAPIView):
    model = RegisterUser
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))

# user register method for Fb

class CreateUserRegisterFB(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', False)
        mob_no = request.data.get('mob_no', False)
        full_name = request.data.get('full_name', False)
        password = request.data.get('password', False)

        if password and full_name:
            pass
        else:
            return Response(errorResponseMethod(request, "Please Enter full_name and Password !"))

        if email:

            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            email_IdValue = str(email)
            if (re.search(regex, email_IdValue)):
                username_qs = User.objects.filter(username=email_IdValue)
                registerUser = RegisterUser.objects.filter(email=email_IdValue)
                if username_qs.exists() and registerUser.exists():
                    return Response(errorResponseMethod(request, "Email Id already exists"))
                else:
                    pass
            else:
                return Response(errorResponseMethod(request, "Invalid Email Id !"))

            RegisterUser.objects.create(
                email=email_IdValue,
                full_name=full_name,
                password=password
            )
            return Response(successResponseMethod(request, 'User register successfully'))

        if mob_no:

            mobileValue = str(mob_no)
            regex = '^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$'
            if (re.search(regex, mobileValue)):

                username_qs = User.objects.filter(username=mobileValue)
                registerUser = RegisterUser.objects.filter(mob_no=mobileValue)
                if username_qs.exists() and registerUser.exists():
                    return Response(errorResponseMethod(request, "mob_no already exists"))
                else:
                    pass

            else:
                return Response(errorResponseMethod(request, "Phone number must be entered in the format: '9999999999',9892799999 Up to 14 digits allowed."))

            RegisterUser.objects.create(
                mob_no=mobileValue,
                full_name=full_name,
                password=password
            )
            return Response(successResponseMethod(request, 'User register successfully'))

# check email id and phone no. before otp verification

class EmaiId_Mobile_no_Verification(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', False)
        mob_no = request.data.get('mob_no', False)

        if email and mob_no:

            # regex1 = '^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$'
            # if (re.search(regex1, mob_no)):
            #     pass
            # else:
            #     return Response(errorResponseMethod(request,
            #                                         "Phone number must be entered in the format: '9999999999',9892799999 Up to 14 digits allowed."))

            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if (re.search(regex, email)):
                username_qs = User.objects.filter(username=email)
                # if username_qs.exists():
                #     pass
                # else:
                #     username_qs = User.objects.filter(username=mob_no)

                registerUser = RegisterUser.objects.filter(email=email)  # , mob_no=mob_no
                if username_qs.exists() and registerUser.exists():
                    return Response(errorResponseMethod(request, "Email Id Already Exists!"))
                    # return Response(
                    #     {"program": "Ecommerce-App", "version": "1.0.0", "release": "",
                    #      "datetime": datetime.datetime.now(),
                    #      "timestamp": datetime.datetime.now().timestamp(), "status": "True", "code": 200,
                    #      "message": "Email Id and Mob_no. Already Exists!",
                    #      "data": []})
                else:
                    pass
                    # return Response(
                    #     {"program": "Ecommerce-App", "version": "1.0.0", "release": "",
                    #      "datetime": datetime.datetime.now(),
                    #      "timestamp": datetime.datetime.now().timestamp(), "status": "False", "code": 200,
                    #      "message": "Mob_no And Email_id Does not Exists!",
                    #      "data": []})

            else:
                return Response(errorResponseMethod(request, "Please Enter Valid Email Id !"))

            regex1 = '^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$'
            if (re.search(regex1, mob_no)):
                username_mo = User.objects.filter(username=mob_no)
                registerUserMobile = RegisterUser.objects.filter(mob_no=mob_no)
                if registerUserMobile.exists() and username_mo.exists():
                    return Response(errorResponseMethod(request, "mob_no Already Exists!"))
                    # return Response(
                    #     {"program": "Ecommerce-App", "version": "1.0.0", "release": "",
                    #      "datetime": datetime.datetime.now(),
                    #      "timestamp": datetime.datetime.now().timestamp(), "status": "True", "code": 200,
                    #      "message": "mob_no Already Exists!",
                    #      "data": []})
                else:
                    pass
            else:
                return Response(errorResponseMethod(request, "Phone number must be entered in the format: '9999999999',9892799999 Up to 14 digits allowed."))

            return Response(
                {"program": "Ecommerce-App", "version": "1.0.0", "release": "",
                 "datetime": datetime.datetime.now(),
                 "timestamp": datetime.datetime.now().timestamp(), "status": "False", "code": 200,
                 "message": "Mob_no And Email_id Does not Exists!",
                 "data": []})

        else:
            return Response(errorResponseMethod(request, "Please Enter email and mob_no !"))


class CreateSuperUserRegister(CreateAPIView):
    model = RegisterUser
    permission_classes = (AllowAny,)
    serializer_class = SuperUserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = SuperUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))


# to get all products , create products, update products, delete products
class ProductDetail(APIView):
    # parser_class = (FileUploadParser,)
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            pk = pk
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get_update_object(self, id):
        try:
            product_category_id = Product.objects.filter(id=id).values('id').annotate(
                product_category_id=F('product_category_id__id'), )
            print(product_category_id[0]['product_category_id'])
            return Product_category.objects.get(id=product_category_id[0]['product_category_id'])
        except Product_category.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, pk=None):
        if pk:
            response = errorResponseMethod(request, "Products are not available or not created yet")
            pk = pk
            # data = ProductView().get_data(pk)
            data = Product.objects.filter(id=pk)
            serializer = GetProductSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        else:
            response = errorResponseMethod(request, "Products are not available or not created yet")
            pk = None
            # data = ProductView().get_data(pk)
            data = Product.objects.all().order_by('-pk')
            serializer = GetProductSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

    def post(self, request, pk=None):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(successResponseMethod(request, serializer.data))
        return Response(errorResponseMethod(request, serializer.errors))

    def put(self, request, pk):
        # pk = ObjectId(pk)
        print(request.data)
        id = pk
        instance = self.get_update_object(id)
        # print("ok in instance")
        # print(instance)
        # print(instance.category_id)
        serializer = ProductCategorySerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))

    def delete(self, request, pk):
        # pk = ObjectId(pk)
        pk = pk
        product = self.get_object(pk)
        product.delete()
        return Response(
            {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
             "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200,
             "message": "Item Deleted ",
             "data": []})


# uplod the image for product
class Product_image_uplod_View(APIView):
    parser_class = (FileUploadParser,)
    permission_classes = (AllowAny,)

    def put(self, request):
        print(request.data)
        try:
            product_id = request.data['product_id']
            product_images = request.data['product_images']
            product = Product.objects.get(product_id=product_id)
        except:
            return Response(errorResponseMethod(request, "Invalid Inputs or Methods"))

        if product:
            product.product_images = product_images
            product.save()
            return Response(
                {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
                 "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200,
                 "message": "Image Uploaded Successfully ",
                 "data": []})
        return Response(errorResponseMethod(request, "Product Id does not Exists"))


# create the order with one product and get the order history of user
class OrderDetail(APIView):
    # parser_class = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk, user_id):
        try:
            pk = pk
            return Order.objects.get(pk=pk, user_id__userId=user_id)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        print(request.user.is_staff)

        print(request.user.is_superuser)
        if pk:
            response = errorResponseMethod(request, "Order Not Created Yet")
            pk = pk
            # data = OrderView().get_data(request, pk, request.user.id)
            data = Order.objects.filter(user_id__userId=request.user.id, id=pk)
            serializer = OrderSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        else:
            response = errorResponseMethod(request, "Order Not Created Yet")
            pk = None
            # print(request.user)
            # print(request.user.id)
            # data = OrderView().get_data(request, pk, request.user.id)
            data = Order.objects.filter(user_id__userId=request.user.id).order_by('-pk')
            serializer = OrderSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

    def post(self, request, pk=None):
        # userId = request.data['user_id']
        try:
            userId = request.data['user_id']
            product_id = request.data['product_id']
        except:
            return Response(errorResponseMethod(request, "Invalid Inputs or Methods"))
        print(request.user.id)
        if userId == request.user.id:
            try:
                registerUserInstance = RegisterUser.objects.get(user_id=userId)
                product = Product.objects.get(product_id=product_id)
            except:
                return Response(errorResponseMethod(request, "User Id or product Id Does not Exists"))
        else:
            return Response(errorResponseMethod(request, "Invalid UserId!"))
        if registerUserInstance and product:
            order, created = Order.objects.get_or_create(user_id=registerUserInstance, status=False)

            order_Product_List, created = Order_Product_List.objects.get_or_create(order_id=order, product_id=product)
            order_Product_List.product_price = product.product_price
            order_Product_List.quantity = (order_Product_List.quantity + 1)

            order_Product_List.save()
            order_Product_List_data = []
            order_Product_List_data = Order_Product_List.objects.filter(order_id=order, product_id=product).values('id',
                                                                                                                   'quantity').annotate(
                username=F('order_id__user_id__userName'),
                product=F('product_id__product_name')
            )

            for orderDetail in order_Product_List_data:
                print(orderDetail)

            return Response(successResponseMethod(request, orderDetail))
        else:
            return Response(errorResponseMethod(request, 'User Id or product id Does not Exists'))

    def delete(self, request, pk):
        # pk = ObjectId(pk)
        pk = pk
        order = self.get_object(pk, request.user.id)
        order.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
             "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200,
             "message": "Item Deleted ",
             "data": []})


# get cart details and add no of quantity for product
class OrderActionDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        if pk:
            response = errorResponseMethod(request, "Order Not Created Yet")
            pk = pk

            data = Order_Product_List.objects.filter(order_id__user_id__userId=request.user.id, id=pk)
            serializer = OrderproductSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        else:
            response = errorResponseMethod(request, "Order Not Created Yet")
            pk = None

            data = Order_Product_List.objects.filter(order_id__user_id__userId=request.user.id)
            serializer = OrderproductSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

    def post(self, request):
        try:
            userId = request.data['user_id']
            product_id = request.data['product_id']
        except:
            return Response(errorResponseMethod(request, "Invalid Inputs or Methods"))
        print(request.user.id)
        if userId == request.user.id:
            try:
                registerUserInstance = RegisterUser.objects.get(user_id=userId)
                product = Product.objects.get(product_id=product_id)
            except:
                return Response(errorResponseMethod(request, "User Id or product Id Does not Exists"))
        else:
            return Response(errorResponseMethod(request, "Invalid UserId!"))
        if registerUserInstance and product:
            order, created = Order.objects.get_or_create(user_id=registerUserInstance, status=False)

            order_Product_List, created = Order_Product_List.objects.get_or_create(order_id=order, product_id=product)
            order_Product_List.product_price = product.product_price
            # order_Product_List.quantity = (order_Product_List.quantity + 1)
            try:
                if request.data['action']:
                    if request.data['action'] == 'add':
                        order_Product_List.quantity = (order_Product_List.quantity + request.data['quantity'])
                        order_Product_List.save()
                    elif request.data['action'] == 'remove':
                        if order_Product_List.quantity >= request.data['quantity']:
                            order_Product_List.quantity = (order_Product_List.quantity - request.data['quantity'])
                            order_Product_List.save()
                        else:
                            return Response(errorResponseMethod(request, "only " + str(
                                order_Product_List.quantity) + " Quantity Available"))

                    elif request.data['action'] == 'increment':
                        order_Product_List.quantity = (order_Product_List.quantity + 1)
                        order_Product_List.save()

                    elif request.data['action'] == 'decrement':
                        if order_Product_List.quantity >= 1:
                            order_Product_List.quantity = (order_Product_List.quantity - 1)
                            order_Product_List.save()
                        else:
                            return Response(errorResponseMethod(request, "only " + str(
                                order_Product_List.quantity) + " Quantity Available"))

                    elif request.data['action'] == 'delete':
                        print("delete method")
                        order_Product_List.delete()
                        return Response(successResponseMethod(request, "Order Deleted"))

                    # order_Product_List.save()

            except:
                return Response(errorResponseMethod(request, "action not provided"))

            # order_Product_List.save()
            order_Product_List_data = []
            order_Product_List_data = Order_Product_List.objects.filter(order_id=order, product_id=product).values('id',
                                                                                                                   'quantity').annotate(
                username=F('order_id__user_id__userName'),
                product=F('product_id__product_name')
            )

            for orderDetail in order_Product_List_data:
                print(orderDetail)

            return Response(successResponseMethod(request, orderDetail))
        else:
            return Response(errorResponseMethod(request, 'User Id or product id Does not Exists'))


# get order history which are delivered for all the users
class OrderHistory(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk=None):
        if pk:
            response = errorResponseMethod(request, "Orders are not placed yet")
            pk = pk
            # data = OrderHistoryView().get_data(pk)
            data = Order.objects.filter(id=pk, order_status='delivered')
            serializer = OrderSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        else:
            response = errorResponseMethod(request, "Orders are not placed yet")
            pk = None
            # data = OrderHistoryView().get_data(pk)
            data = Order.objects.filter(order_status='delivered')
            serializer = OrderSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)


# register and update the shipping address
class ShippingAddress(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            pk = pk
            return Shipping_address.objects.get(pk=pk)
        except Shipping_address.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            response = errorResponseMethod(request, "Address Not Register Yet")
            pk = pk

            data = Shipping_address.objects.filter(user_id__userId=request.user.id, id=pk)
            serializer = ShippingAddressSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        else:
            response = errorResponseMethod(request, "Address Not Register Yet")
            pk = None

            data = Shipping_address.objects.filter(user_id__userId=request.user.id)
            serializer = ShippingAddressSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

    def post(self, request, pk=None):
        print(request.data)
        try:
            userId = request.data['user_id']

        except:
            return Response(errorResponseMethod(request, "Invalid Inputs or Methods"))

        print(request.user.id)
        if userId == request.user.id:
            try:
                shipping_address = Shipping_address.objects.filter(user_id__userId=userId).exists()
                getUser = RegisterUser.objects.get(userId=userId)
                print(getUser)

                if shipping_address:
                    return Response(errorResponseMethod(request,
                                                        "Shipping Address is already register for this user!, You Can Update Our Address"))
                else:
                    serializer = ShippingAddressSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        print(serializer.data)
                        Shipping_address.objects.filter(id=serializer.data['id']).update(user_id=getUser)
                        return Response(successResponseMethod(request, serializer.data))

                    return Response(errorResponseMethod(request, serializer.errors))

            except:
                pass
        else:
            return Response(errorResponseMethod(request, "Invalid UserId!"))

    def put(self, request, pk):
        # pk = ObjectId(pk)
        print(request.data)
        id = pk
        instance = self.get_object(id)
        print(instance)
        serializer = ShippingAddressSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))

    def delete(self, request, pk):
        # pk = ObjectId(pk)
        pk = pk
        shipping_address = self.get_object(pk)
        shipping_address.delete()
        return Response(
            {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
             "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200,
             "message": "Address Deleted ",
             "data": []})


# create and update offer details
class OfferDetails(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            pk = pk
            return Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            response = errorResponseMethod(request, "Offer not available Yet")
            pk = pk

            data = Offer.objects.filter(id=pk)
            serializer = OfferSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        else:
            response = errorResponseMethod(request, "Offer not available Yet")
            pk = None

            data = Offer.objects.all()
            print(data)
            serializer = OfferSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

    def post(self, request, pk=None):
        print(request.data)

        print(request.user.id)

        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)

            return Response(successResponseMethod(request, serializer.data))
        return Response(errorResponseMethod(request, serializer.errors))

    def put(self, request, pk):
        # pk = ObjectId(pk)
        print(request.data)
        id = pk
        instance = self.get_object(id)
        print(instance)
        serializer = OfferSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))

    def delete(self, request, pk):
        # pk = ObjectId(pk)
        pk = pk
        offer = self.get_object(pk)
        offer.delete()
        return Response(
            {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
             "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200,
             "message": "Offer Deleted ",
             "data": []})


class Offer_Apply(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        now = datetime.datetime.now()
        print(request.data)
        try:
            userId = request.data['user_id']
            cartQuantity = request.data['cartQuantity']
            promo_code = request.data['promo_code']
        except:
            return Response(errorResponseMethod(request, "Invalid Inputs or Methods"))
        print(request.user.id)
        if userId == request.user.id:
            try:
                registerUserInstance = RegisterUser.objects.get(userId=userId)  # user_id
                # product = Product.objects.get(product_id=product_id)
            except:
                return Response(errorResponseMethod(request, "User Id Does not Exists"))
        else:
            return Response(errorResponseMethod(request, "Invalid UserId!"))
        if registerUserInstance:
            order, created = Order.objects.get_or_create(user_id=registerUserInstance, status=False)

            # order_Product_List, created = Order_Product_List.objects.get_or_create(order_id=order, product_id=product)
            try:
                print(now)
                offer = Offer.objects.get(promo_code__iexact=promo_code,
                                          offer_start_date__lte=now,
                                          offer_end_date__gte=now,
                                          status=True
                                          )
                print(offer)
            except:
                return Response(errorResponseMethod(request, 'promocode Does not Exists'))
            print("quantity checking")
            # print(order_Product_List.quantity)
            print(order.get_cart_quantities)
            print(offer.offers_on_product)
            if int(cartQuantity) >= offer.offers_on_product:  # order.get_cart_quantities
                print("checking before offer appy")
                print(order.offer_Id)
                if request.user.id == 2:
                    order.offer_Id = offer
                    order.discount = offer.discount
                    order.save()
                elif order.offer_Id is None:
                    order.offer_Id = offer
                    order.discount = offer.discount
                    order.save()
                else:
                    return Response(errorResponseMethod(request, "This Promo Code Is Used "))
            else:
                return Response(errorResponseMethod(request, "offer is valid for minimum " + str(
                    offer.offers_on_product) + " quantity"))

            # print(offer.discount)

            return Response(
                successResponseMethod(request, {"discount": offer.discount}))  # "Promo Code Applied Successfully"
        else:
            return Response(errorResponseMethod(request, 'User Id or product id Does not Exists'))


# get create and update delivery boy data
class DeliveryBoyData(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            pk = pk
            return Delivery_boy_data.objects.get(pk=pk)
        except Delivery_boy_data.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            response = errorResponseMethod(request, "Delivery Boy Not Register Yet")
            pk = pk

            data = Delivery_boy_data.objects.filter(id=pk)
            serializer = DeliveryBoySerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        else:
            response = errorResponseMethod(request, "Delivery Boy Not Register Yet")
            pk = None

            data = Delivery_boy_data.objects.all()
            serializer = DeliveryBoySerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

    def post(self, request, pk=None):
        print(request.data)

        serializer = DeliveryBoySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data)
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))

    def put(self, request, pk):
        # pk = ObjectId(pk)
        print(request.data)
        id = pk
        instance = self.get_object(id)
        print(instance)
        serializer = DeliveryBoySerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))

    def delete(self, request, pk):
        # pk = ObjectId(pk)
        pk = pk
        deliveryBoy = self.get_object(pk)
        deliveryBoy.delete()
        return Response(
            {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
             "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200,
             "message": "delivery Boy Deleted ",
             "data": []})


# sign up vender register
class CreateVendorManagement(CreateAPIView):
    model = Vendor_management
    permission_classes = (AllowAny,)
    serializer_class = VendorManagementSerializer

    def post(self, request, *args, **kwargs):
        serializer = VendorManagementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))


# get and update vendor details
class VendorManagementDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            pk = pk
            return Vendor_management.objects.get(pk=pk)
        except Vendor_management.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            response = errorResponseMethod(request, "Vendor Not Register Yet")
            pk = pk

            data = Vendor_management.objects.filter(vendor_id=request.user.id, id=pk)
            serializer = GetVendorManagementSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        else:
            response = errorResponseMethod(request, "Vendor Not Register Yet")
            pk = None

            data = Vendor_management.objects.filter(vendor_id=request.user.id)
            serializer = GetVendorManagementSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

    def put(self, request, pk):
        print(request.data)
        id = pk
        instance = self.get_object(id)
        print(instance)
        serializer = GetVendorManagementSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))

    def delete(self, request, pk):
        pk = pk
        venderManagement = self.get_object(pk)
        venderManagement.delete()
        return Response(
            {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
             "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200,
             "message": "Vendor Deleted ",
             "data": []})


# get or create vendor stock details
class VendorStockDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk, user_id):
        try:
            pk = pk
            return Vendor_Stock.objects.get(pk=pk, vendor_id__vendor_id=user_id)
        except Vendor_Stock.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        print(request.user.is_staff)
        if request.user.is_staff:

            if pk:
                response = errorResponseMethod(request, "Vendor Stock Not Created Yet")
                pk = pk
                # data = OrderView().get_data(request, pk, request.user.id)
                data = Vendor_Stock.objects.filter(vendor_id__vendor_id=request.user.id, id=pk)
                serializer = VendorStockSerializer(data, many=True)
                if data:
                    response = successResponseMethod(request, serializer.data)
                return Response(response)

            else:
                response = errorResponseMethod(request, "Vendor Stock Not Created Yet")
                pk = None
                # print(request.user)
                # print(request.user.id)
                # data = OrderView().get_data(request, pk, request.user.id)
                data = Vendor_Stock.objects.filter(vendor_id__vendor_id=request.user.id)
                serializer = VendorStockSerializer(data, many=True)
                if data:
                    response = successResponseMethod(request, serializer.data)
                return Response(response)

        else:
            return Response(errorResponseMethod(request, "this is only for vendors "))

    def post(self, request, pk=None):
        if request.user.is_staff:

            serializer = VendorStockSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                Vendor_Stock.objects.filter(id=serializer.data['id']).update(vendor_id=Vendor_management.objects.get(vendor_id=request.user.id))

                data = Vendor_Stock.objects.filter(vendor_id__vendor_id=request.user.id, id=serializer.data['id'])
                serializer1 = VendorStockSerializer(data, many=True)
                if data:
                    return Response(successResponseMethod(request, serializer1.data))

                return Response(successResponseMethod(request, serializer.data))

            return Response(errorResponseMethod(request, serializer.errors))

        else:
            return Response(errorResponseMethod(request, "this is only for vendors "))

    def put(self, request, pk):
        if request.user.is_staff:
            id = pk
            instance = self.get_object(id, request.user.id)
            print(instance)
            serializer = VendorStockSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return Response(successResponseMethod(request, serializer.data))

            return Response(errorResponseMethod(request, serializer.errors))
        else:
            return Response(errorResponseMethod(request, "this is only for vendors "))


    def delete(self, request, pk):
        if request.user.is_staff:
            id = pk
            # vendorStock = self.get_object(pk)
            vendorStock = self.get_object(id, request.user.id)
            vendorStock.delete()
            return Response(
                {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
                    "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200,
                    "message": "vendorStock Deleted ",
                    "data": []})
        else:
            return Response(errorResponseMethod(request, "this is only for vendors "))

class GetOnlyVendorStockDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk, user_id):
        try:
            pk = pk
            return Vendor_Stock.objects.get(pk=pk, vendor_id__vendor_id=user_id)
        except Vendor_Stock.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        print(request.user.is_staff)
        if request.user.is_staff:

            if pk:
                response = errorResponseMethod(request, "Vendor Stock Not Created Yet")
                pk = pk

                # data = Vendor_Stock.objects.filter(vendor_id__vendor_id=request.user.id, id=pk)
                data = Vendor_Stock.objects.filter(vendor_id__vendor_id=request.user.id, id=pk).values('id', 'quantity',
                                                                                                'price',
                                                                                                'selling_price',
                                                                                                'status').annotate(
                    product_id=F('product_id__product_name'),
                    product_category_id=F('product_category_id__category_name'),
                )
                # serializer = VendorStockSerializer(data, many=True)
                if data:
                    response = successResponseMethod(request, data)
                return Response(response)

            else:
                response = errorResponseMethod(request, "Vendor Stock Not Created Yet")
                pk = None

                data = Vendor_Stock.objects.filter(vendor_id__vendor_id=request.user.id).values('id', 'quantity', 'price',
                                                                                                'selling_price', 'status').annotate(
                    product_id = F('product_id__product_name'),
                    product_category_id = F('product_category_id__category_name'),
                )
                print(data)
                # serializer = VendorStockSerializer(data, many=True)
                if data:
                    response = successResponseMethod(request, data)
                return Response(response)
        else:
            return Response(errorResponseMethod(request, "this is only for vendors "))


# get or create product category
class ProductCategoryDetails(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            pk = pk
            return Product_category.objects.get(pk=pk)
        except Product_category.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            response = errorResponseMethod(request, "Product Category Not Register Yet")
            pk = pk

            data = Product_category.objects.filter(id=pk)
            serializer = Product_CategorySerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        else:
            response = errorResponseMethod(request, "Product Category Not Register Yet")
            pk = None

            data = Product_category.objects.all().order_by('-pk')
            serializer = Product_CategorySerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

    def post(self, request, pk=None):
        print(request.data)

        serializer = Product_CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data)
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))

    def put(self, request, pk):
        # pk = ObjectId(pk)
        print(request.data)
        id = pk
        instance = self.get_object(id)
        print(instance)
        serializer = Product_CategorySerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))

    def delete(self, request, pk):
        # pk = ObjectId(pk)
        pk = pk
        productCategory = self.get_object(pk)
        productCategory.delete()
        return Response(
            {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
             "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200,
             "message": "productCategory Deleted ",
             "data": []})


# Drop Down API For Product Category
class SelectProductCatrgory(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        response = errorResponseMethod(request, "Product Category Not Available")

        data = Product_category.objects.all().order_by('-pk')
        print(data)
        serializer = SelectProductCatrgorySerializer(data, many=True)
        if data:
            response = successResponseMethod(request, serializer.data)
        return Response(response)

# Drop Down API For Product
class SelectProduct(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        response = errorResponseMethod(request, "Product Not Available")

        data = Product.objects.all().order_by('-pk')
        print(data)
        serializer = SelectProductSerializer(data, many=True)
        if data:
            response = successResponseMethod(request, serializer.data)
        return Response(response)


# get or create the product
class productDetailsView(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            pk = pk
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        print(request.data)
        if pk:
            response = errorResponseMethod(request, "Product Not Register Yet")
            pk = pk

            data = Product.objects.filter(id=pk)
            serializer = Product_viewSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        else:
            response = errorResponseMethod(request, "Product Not Register Yet")
            pk = None

            data = Product.objects.all().order_by('-pk')
            print(data)
            serializer = Product_viewSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

    def post(self, request, pk=None):
        print(request.data)

        serializer = Product_viewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data)
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))

    def put(self, request, pk):
        # pk = ObjectId(pk)
        print(request.data)
        id = pk
        instance = self.get_object(id)
        print(instance)
        serializer = Product_viewSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))

    def delete(self, request, pk):
        # pk = ObjectId(pk)
        pk = pk
        product = self.get_object(pk)
        product.delete()
        return Response(
            {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
             "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200,
             "message": "product Deleted ",
             "data": []})


class ProductSearchAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = Product_viewSerializer
    # authentication_classes = (AllowAny,)
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ('-created_at')
    # or_lookup = (Q('product_name__icontains=queryset'))
    search_fields = (
        'product_id', 'product_category_id__category_name', 'product_name', 'product_description', 'product_price',
        'product_status', 'discount', 'rating', 'status')


class HomePageContentAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk=None):
        print(request.data)

        response = errorResponseMethod(request, "Product Not Register Yet")
        pk = None
        data = getHomePageContent.get_data(self, pk)
        if data:
            response = successResponseMethod(request, data)
        return Response(response)


class GetProductByCategory(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk=None):
        print(request.data)

        response = errorResponseMethod(request, "Product Not Register Yet")
        pk = pk
        print(pk)
        data = getProductByCategoryView.get_data(self, pk)

        serializer = Product_viewSerializer(data, many=True)
        if data:
            response = successResponseMethod(request, serializer.data)
        return Response(response)


class GetOneProductDetailsAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk=None):
        print(request.data)

        response = errorResponseMethod(request, "Product Not Register Yet")
        pk = pk
        print(pk)
        data = getOneProductDetailsView.get_data(self, pk)

        serializer = Product_viewSerializer(data, many=True)
        if data:
            response = successResponseMethod(request, serializer.data)
        return Response(response)


# get the user register details and update the details
class UserRegisterDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            pk = pk
            return RegisterUser.objects.get(pk=pk)
        except RegisterUser.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            response = errorResponseMethod(request, "User Not Register Yet")
            pk = pk

            data = RegisterUser.objects.filter(userId=request.user.id, id=pk)
            serializer = GetUserRegisterSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        else:
            response = errorResponseMethod(request, "User Not Register Yet")
            pk = None

            data = RegisterUser.objects.filter(userId=request.user.id)
            serializer = GetUserRegisterSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

    def put(self, request, pk):
        print(request.data)
        id = pk
        instance = self.get_object(id)
        print(instance)
        serializer = GetUserRegisterSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))


class UserProfileImageUpload(APIView):
    parser_class = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.data)

        try:
            userId = request.data['userId']
        except:
            return Response(errorResponseMethod(request, "UserId Not Provided !"))

        if int(userId) == request.user.id:
            try:
                image = request.data['image']
                registerUser = RegisterUser.objects.get(userId=request.user.id)
            except:
                return Response(errorResponseMethod(request, "Invalid Inputs or Methods"))
        else:
            return Response(errorResponseMethod(request, "Invalid userId"))

        if registerUser:
            registerUser.image = image
            registerUser.save()
            response = errorResponseMethod(request, "userId does not Exists")
            data = RegisterUser.objects.filter(userId=request.user.id)
            serializer = GetUserRegisterSerializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        return Response(errorResponseMethod(request, "userId does not Exists"))


# change password
class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        userId = request.data.get('userId', False)
        new_password = request.data.get('new_password', False)
        old_password = request.data.get('old_password', False)
        vendor_id = request.data.get('vendor_id', False)

        if request.user.is_staff:
            if int(vendor_id) == request.user.id:
                userInstance = User.objects.get(username=request.user)
                registerVendorManagementInstance = Vendor_management.objects.get(user=userInstance,
                                                                                 vendor_id=request.user.id)
            else:
                return Response(errorResponseMethod(request, "vendor_id does not Exists"))

            if new_password:

                msg = 'Note: password is as least 6 characters long and has at least 2 digits and 1 Upper case letter'
                min_length = 6

                if len(new_password) < min_length:
                    return Response(errorResponseMethod(request, 'Password must be at least {0} characters '
                                                                 'long.'.format(min_length) + msg))

                # if len(new_password) > 20:
                #     return Response(errorResponseMethod(request, 'Password not more then 20 characters '
                #                                                  'long.'.format(min_length) + msg))
                #
                # # check for 2 digits
                # if sum(c.isdigit() for c in new_password) < 2:
                #     return Response(errorResponseMethod(request, 'Password must contain at least 2 digits.' + msg))
                #
                # # check for uppercase letter
                # if not any(c.isupper() for c in new_password):
                #     return Response(
                #         errorResponseMethod(request, 'Password must container at least 1 uppercase letter.' + msg))
            else:
                return Response(
                    errorResponseMethod(request, 'Please Enter The New Password'))

            if userInstance and registerVendorManagementInstance:
                # Check old password
                if not userInstance.check_password(request.data.get("old_password")):
                    return Response(errorResponseMethod(request, "old_password not exists"))
                # set_password also hashes the password that the user will get
                userInstance.set_password(request.data.get("new_password"))
                registerVendorManagementInstance.password = request.data.get("new_password")
                userInstance.save()
                registerVendorManagementInstance.save()

                return Response(successResponseMethod(request, 'Password updated successfully'))

            return Response(errorResponseMethod(request, "vendor_id does not Exists"))

        else:
            if int(userId) == request.user.id:
                userInstance = User.objects.get(username=request.user)
                registerUserInstance = RegisterUser.objects.get(user=userInstance, userId=request.user.id)
            else:
                return Response(errorResponseMethod(request, "userId does not Exists"))

            if new_password:

                msg = 'Note: password is as least 6 characters long and has at least 2 digits and 1 Upper case letter'
                min_length = 6

                if len(new_password) < min_length:
                    return Response(errorResponseMethod(request, 'Password must be at least {0} characters '
                                                                 'long.'.format(min_length) + msg))

                # if len(new_password) > 20:
                #     return Response(errorResponseMethod(request, 'Password not more then 20 characters '
                #                                                  'long.'.format(min_length) + msg))
                #
                # # check for 2 digits
                # if sum(c.isdigit() for c in new_password) < 2:
                #     return Response(errorResponseMethod(request, 'Password must contain at least 2 digits.' + msg))
                #
                # # check for uppercase letter
                # if not any(c.isupper() for c in new_password):
                #     return Response(
                #         errorResponseMethod(request, 'Password must container at least 1 uppercase letter.' + msg))
            else:
                return Response(
                    errorResponseMethod(request, 'Please Enter The New Password'))

            if userInstance and registerUserInstance:
                # Check old password
                if not userInstance.check_password(request.data.get("old_password")):
                    return Response(errorResponseMethod(request, "old_password not exists"))
                # set_password also hashes the password that the user will get
                userInstance.set_password(request.data.get("new_password"))
                registerUserInstance.password = request.data.get("new_password")
                userInstance.save()
                registerUserInstance.save()

                return Response(successResponseMethod(request, 'Password updated successfully'))

            return Response(errorResponseMethod(request, "userId does not Exists"))

#forgot password
class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # username = request.data.get('username', False)
        mob_no = request.data.get('mob_no', False)

        try:
            userInstance = User.objects.get(username=mob_no)
            registerUserInstance = RegisterUser.objects.filter(user=userInstance, mob_no=mob_no)
        except:
            return Response(errorResponseMethod(request, "mob_no does not Exists"))

        if userInstance and registerUserInstance:
            details = registerUserInstance.values('id', 'userId', 'full_name', 'email', 'mob_no')
            print(details)
            return Response(successResponseMethod(request, details[0]))
        else:
            return Response(errorResponseMethod(request, "user does not Exists"))

#change forgot password
class ForgotPasswordResetView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        userId = request.data.get('userId', False)
        new_password = request.data.get('new_password', False)

        try:
            userInstance = User.objects.get(id=userId)
            registerUserInstance = RegisterUser.objects.get(user=userInstance, userId=userId)
        except:
            return Response(errorResponseMethod(request, "userId does not Exists"))

        if userInstance and registerUserInstance:
            if new_password:
                msg = 'Note: password is as least 6 characters long and has at least 2 digits and 1 Upper case letter'
                min_length = 6

                if len(new_password) < min_length:
                    return Response(errorResponseMethod(request, 'Password must be at least {0} characters '
                                                                 'long.'.format(min_length) + msg))

                # if len(new_password) > 20:
                #     return Response(errorResponseMethod(request, 'Password not more then 20 characters '
                #                                                  'long.'.format(min_length) + msg))
                #
                # # check for 2 digits
                # if sum(c.isdigit() for c in new_password) < 2:
                #     return Response(errorResponseMethod(request, 'Password must contain at least 2 digits.' + msg))
                #
                # # check for uppercase letter
                # if not any(c.isupper() for c in new_password):
                #     return Response(
                #         errorResponseMethod(request, 'Password must container at least 1 uppercase letter.' + msg))
            else:
                return Response(
                    errorResponseMethod(request, 'Please Enter The New Password'))

            if userInstance and registerUserInstance:
                # Check old password
                # if not userInstance.check_password(request.data.get("old_password")):
                #     return Response(errorResponseMethod(request, "old_password not exists"))
                # set_password also hashes the password that the user will get
                userInstance.set_password(request.data.get("new_password"))
                registerUserInstance.password = request.data.get("new_password")
                userInstance.save()
                registerUserInstance.save()

                return Response(successResponseMethod(request, 'Password updated successfully'))
        else:
            return Response(errorResponseMethod(request, "user does not Exists"))


# register User Email id
class AddUserEmail(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', False)
        userId = request.data.get('userId', False)

        if int(userId) == request.user.id:
            try:
                userInstance = User.objects.get(username=request.user)
                registerUserInstance = RegisterUser.objects.get(user=userInstance, userId=request.user.id)
            except:
                return Response(errorResponseMethod(request, "User Not exists"))

            if userInstance and registerUserInstance:
                userInstance.email = email
                registerUserInstance.email = email
                userInstance.save()
                registerUserInstance.save()
                registerUserInstance = RegisterUser.objects.filter(user=userInstance, userId=request.user.id).values(
                    'id', 'userId', 'email', 'mob_no', 'full_name'
                )
                return Response(successResponseMethod(request, registerUserInstance[0]))
            else:
                return Response(errorResponseMethod(request, "Something Went wrong"))
        else:
            return Response(errorResponseMethod(request, "Invalid userId"))


# forgor password to get email
# class ForgotPasswordView(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         # username = request.data.get('username', False)
#         email = request.data.get('email', False)
#
#         try:
#             # userInstance = User.objects.get(username=username)
#             userInstance = User.objects.get(email=email)
#         except:
#             return Response(errorResponseMethod(request, "email Id does not Exists"))
#
#         print(userInstance.is_staff)
#
#         if userInstance.is_staff:
#             try:
#                 getPassword = Vendor_management.objects.filter(email=email, user=userInstance).values('vendor_id')
#                 vendor_id = str(getPassword[0].get('userId'))
#                 base_host_url = request.get_host()
#                 passResetUrl = '/dashboard/ForgotPasswordView/' + vendor_id + '/'
#                 baseUrl = 'http://' + base_host_url + passResetUrl
#                 msz = 'Forgotten your password? \nEnter your username and New password on this link. \n ' + baseUrl
#
#                 # return Response(successResponseMethod(request, getPassword[0].get('password')))
#                 try:
#                     email = EmailMessage("Reset Password", msz, to=[userInstance.email])
#                     email.send()
#                     ms = "We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly."
#                     return Response(successResponseMethod(request, ms))
#
#                 except:
#                     return Response(errorResponseMethod(request, "something went wrong !"))
#
#             except:
#                 return Response(errorResponseMethod(request, "email Id does not Exists"))
#         else:
#             try:
#                 getPassword = RegisterUser.objects.filter(email=email, user=userInstance).values('userId')
#                 userId = str(getPassword[0].get('userId'))
#                 # print(userId)
#                 base_host_url = request.get_host()
#                 # print(base_host_url)
#                 passResetUrl = '/dashboard/ForgotPasswordView/'+userId+'/'
#                 # print(passResetUrl)
#                 baseUrl = 'http://' + base_host_url + passResetUrl
#                 # print(baseUrl)
#
#                 msz = 'Forgotten your password? \nEnter your username and New password on this link. \n '+baseUrl
#                 try:
#                     email = EmailMessage("Reset Password", msz, to=[userInstance.email])
#                     email.send()
#                     ms = "We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly."
#                     return Response(successResponseMethod(request, ms))
#
#                 except:
#                     return Response(errorResponseMethod(request, "something went wrong !"))
#
#             except:
#                 return Response(errorResponseMethod(request, "email Id does not Exists"))

# mobile no validation during registration process
# send otp while registering
class ValidatePhoneSendOTP(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # name = request.data.get('name' , False)
        phone_number = request.data.get('phone', False)

        regex = '^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$'
        if (re.search(regex, phone_number)):
            pass
        else:
            return Response({
                'status': False,
                'detail': "Phone number must be entered in the format: '9999999999',9892799999 Up to 14 digits allowed."
            })

        if phone_number:
            phone = str(phone_number)
            # user = User.objects.filter(phone__iexact = phone)
            user = RegisterUser.objects.filter(mob_no__iexact=phone)

            if user.exists():
                return Response({
                    'status': False,
                    'detail': 'Phone number already exists.'
                })
            else:
                key = send_otp(phone)

                if key:
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        # if count > 10:
                        #     print("limit try")
                        old.count = count + 1
                        old.otp = key
                        old.save()
                        print(count)
                        print(key)
                        return Response({
                            'status': True,
                            'detail': 'OTP sent successfully.'
                        })
                    else:
                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=key,
                        )
                        print(key)
                        return Response({
                            'status': True,
                            'detail': 'OTP sent successfully.'
                        })

                else:
                    return Response({
                        'status': False,
                        'detail': 'Sending OTP error.'
                    })

        else:
            return Response({
                'status': False,
                'detail': 'Phone number is not given in post request.'
            })


def send_otp(phone):
    if phone:
        key = random.randint(999, 9999)
        print(key)
        return key
    else:
        return False


# Validate otp for registration
class ValidateOTP(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            print(old)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    return Response({
                        'status': True,
                        'datail': 'OTP Matched. Please Proceed For Registration'
                    })

                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP Incorect'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'First Proceed Via Sending Otp Request'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Please Provide Both Phone And Otp For Validation'
            })


# this is use for product subscribe
class ProductSubscribe(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            pk = pk
            return Product_Subscribe.objects.get(pk=pk)
        except Product_Subscribe.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        print(request.data)
        if pk:
            response = errorResponseMethod(request, "Product Subscribe Not Register Yet")
            pk = pk

            data = Product_Subscribe.objects.filter(id=pk, user_id__userId=request.user.id)
            serializer = Product_subscribe_serializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

        else:
            response = errorResponseMethod(request, "Product Subscribe Not Register Yet ")
            pk = None

            data = Product_Subscribe.objects.filter(user_id__userId=request.user.id).order_by('-pk')
            print(data)
            serializer = Product_subscribe_serializer(data, many=True)
            if data:
                response = successResponseMethod(request, serializer.data)
            return Response(response)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', False)
        product_id = request.data.get('product_id', False)

        try:
            registerUserInstance = RegisterUser.objects.get(userId=user_id)
            productInstance = Product.objects.get(product_id=product_id)
        except:
            return Response(errorResponseMethod(request, "Invalid user_id or product_id"))

        if Product_Subscribe.objects.filter(product_id=productInstance).exists():
            return Response(errorResponseMethod(request, "you have already subscribe for this product"))
        else:
            pass
        del request.data['user_id']
        del request.data['product_id']
        print(request.data)
        serializer = Product_subscribe_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            Product_Subscribe.objects.filter(id=serializer.data['id']).update(user_id=registerUserInstance,
                                                                              product_id=productInstance)
            data = Product_Subscribe.objects.filter(id=serializer.data['id'])
            serializer = Product_subscribe_serializer(data, many=True)
            return Response(successResponseMethod(request, serializer.data))
        return Response(errorResponseMethod(request, serializer.errors))

    def put(self, request, pk):
        print(request.data)
        id = pk
        instance = self.get_object(id)
        print(instance)
        serializer = Product_subscribe_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(successResponseMethod(request, serializer.data))

        return Response(errorResponseMethod(request, serializer.errors))

    def delete(self, request, pk):
        pk = pk
        product_Subscribe = self.get_object(pk)
        product_Subscribe.delete()
        return Response(
            {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
             "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200,
             "message": "product_Subscribe Deleted ",
             "data": []})


# this is used for product subscription resume and stop
class ProductSubscribeStopeAndResume(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk, userId):
        try:
            pk = pk
            return Product_Subscribe.objects.get(pk=pk, user_id__userId=userId)
        except Product_Subscribe.DoesNotExist:
            raise Http404

    def post(self, request, pk=None):
        product_Subscribe = self.get_object(pk, request.user.id)
        # product_Subscribe.status = True
        print(product_Subscribe.status)
        if product_Subscribe.status == True:
            print("in true")
            product_Subscribe.status = False
        elif product_Subscribe.status == False:
            print("in false")
            product_Subscribe.status = True
        product_Subscribe.save()

        data = Product_Subscribe.objects.filter(id=pk, user_id__userId=request.user.id)
        serializer = Product_subscribe_serializer(data, many=True)
        if data:
            return Response(
                {"program": "Ecommerce-App", "version": "1.0.0", "release": "", "datetime": datetime.datetime.now(),
                 "timestamp": datetime.datetime.now().timestamp(), "status": "success", "code": 200,
                 "message": "product_Subscribe Resume ! ",
                 "data": serializer.data})
        return Response(errorResponseMethod(request, "Something went wrong !"))


# place order from mobile application
class placeOrderView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', False)
        products = request.data.get('products', False)
        subTotal = request.data.get('subTotal', False)
        deliveryCharges = request.data.get('deliveryCharges', False)
        taxCharges = request.data.get('taxCharges', False)
        discount = request.data.get('discount', False)
        discountCouponCode = request.data.get('discountCouponCode', False)
        grandTotal = request.data.get('grandTotal', False)
        deliveryAddress = request.data.get('deliveryAddress', False)
        payment_mode = request.data.get('payment_mode', False)

        if int(user_id) == request.user.id:
            try:
                registerUserInstance = RegisterUser.objects.get(user_id=request.user.id)
                print(registerUserInstance)
                order, created = Order.objects.get_or_create(status=False, user_id=registerUserInstance)
                print(order)
            except:
                return Response(errorResponseMethod(request, "User Id Does not Exists Or Someting Went Wrong !"))
        else:
            return Response(errorResponseMethod(request, "Invalid User Id!"))

        if products and order:
            print(products)

            for product in products:
                productInstance = Product.objects.get(product_id=product.get('product_id'))
                order_Product_List, created = Order_Product_List.objects.get_or_create(order_id=order,
                                                                                       product_id=productInstance)
                order_Product_List.product_price = productInstance.product_price
                order_Product_List.quantity = product.get('quantity')
                order_Product_List.save()
        else:
            return Response(errorResponseMethod(request, "Please Enter Products"))

        if order.offer_Id is None:
            order.subTotal = subTotal
            order.deliveryCharges = deliveryCharges
            order.taxCharges = taxCharges
            order.grandTotal = grandTotal
            order.payment_mode = payment_mode
            # order.status = True
            # order.order_status = 'delivered'
            # order.save()
        else:
            order.discount = discount
            order.discountCouponCode = discountCouponCode
            order.subTotal = subTotal
            order.deliveryCharges = deliveryCharges
            order.taxCharges = taxCharges
            order.grandTotal = grandTotal
            order.payment_mode = payment_mode
            # order.status = True
            # order.order_status = 'delivered'
            # order.save()

        if deliveryAddress:

            instance, created = Shipping_address.objects.get_or_create(user_id=registerUserInstance)
            # print(instance)
            serializer = ShippingAddressSerializer(instance, data=deliveryAddress)
            if serializer.is_valid():
                serializer.save()
                order.status = True
                order.order_status = 'delivered'
                order.save()
                return Response(successResponseMethod(request, "Successfully Added All the details"))
            return Response(errorResponseMethod(request, serializer.errors))

        return Response(errorResponseMethod(request, "Please Enter Delivery Address"))


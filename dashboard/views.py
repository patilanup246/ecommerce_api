from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.contrib.auth.models import User
from dashboard.productModel import Product, Product_category
from dashboard.orderModel import Order, Order_Product_List
from dashboard.userModel import RegisterUser
from dashboard.vendorModel import Vendor_management
from django.db.models import (Case, CharField, Count, DateTimeField,
                              ExpressionWrapper, F, FloatField, Func, Max, Min,
                              Prefetch, Q, Sum, Value, When, Subquery)
from django.db.models import Subquery
from copy import deepcopy
import json
import requests


# get user and vendor details with toten id
class GetCurrentUserWithToken(View):
    def get_data(self, username):
        data = {}
        user = User.objects.get(username=username)
        user_ID = User.objects.filter(username=username).values('id')
        registerUser = RegisterUser.objects.filter(user=user, userId=user_ID[0]['id'])

        data.update({"user": [{"id": userData.id,
                               "userId": userData.userId,
                               # "userName":userData.userName,
                               # "first_name":userData.first_name,
                               # "last_name":userData.last_name,
                               # "email":userData.email,
                               "full_name": userData.full_name,
                               "mob_no": userData.mob_no,
                               "wallet_amount": userData.wallet_amount,
                               "user_images_URL": userData.user_images_URL,
                               }
                              for userData in registerUser]})
        print(data)
        return data

    def get_VendorManagementData(self, user_id):
        data = {}
        user = User.objects.get(username=user_id)
        vendor_ID = User.objects.filter(username=user_id).values('id')

        vendor_management = Vendor_management.objects.filter(user=user, vendor_id=vendor_ID[0]['id'])

        data.update({"user": [{
            "id": vendorData.id,
            "vendor_id": vendorData.vendor_id,
            "userName": vendorData.userName,
            "first_name": vendorData.first_name,
            "last_name": vendorData.last_name,
            "email": vendorData.email,
            "mob_no": vendorData.mob_no,
            "image": vendorData.image,
        }
            for vendorData in vendor_management]})
        print(data)
        return data


class CurrentUser(View):
    def get_data(self, username):
        data = {}
        user = User.objects.get(username=username)
        data = User.objects.filter(username=username).values('id')
        registerUser = RegisterUser.objects.filter(user=user, userId=data[0]['id']).values('id', 'userId', 'full_name',
                                                                                           'mob_no', 'wallet_amount')

        return list(registerUser)

    def get_VendorManagementData(self, user_id):
        data = {}
        user = User.objects.get(username=user_id)
        data = User.objects.filter(username=user_id).values('id', 'username', 'password', 'first_name', 'last_name')
        vendor_management = Vendor_management.objects.filter(user=user, vendor_id=data[0]['id']).values('id',
                                                                                                        'vendor_id',
                                                                                                        'userName',
                                                                                                        'first_name',
                                                                                                        'last_name',
                                                                                                        'email',
                                                                                                        'mob_no')

        return list(vendor_management)


class getHomePageContent(View):
    def get_data(self, pk):
        data = {}
        features = Product.objects.all().order_by('-pk')[0:3]
        trending_products = Product.objects.all().order_by('-pk')
        product_category = Product_category.objects.all().order_by('-pk')
        # print(product_category)

        data.update({
            "features": [{"id": value.id, "img": value.product_images_URL} for value in features],
            "trending_products": [{"id": value1.id,
                                   "product_id": value1.product_id,
                                   # "product_category_id":value1.product_category_id,
                                   "product_name": value1.product_name,
                                   "product_description": value1.product_description,
                                   "product_images_URL": value1.product_images_URL,
                                   "product_price": value1.product_price,
                                   "product_status": value1.product_status,
                                   "discount": value1.discount,
                                   "rating": value1.rating,
                                   "status": value1.status,
                                   "created_at": value1.created_at,
                                   "updated_at": value1.updated_at,

                                   }
                                  for value1 in trending_products],
            "product_category": [{
                "id": value2.id,
                "category_id": value2.category_id,
                "category_name": value2.category_name,
                "category_description": value2.category_description,
                "product_thumbnail": value2.product_thumbnail_URL,
                "status": value2.status,
                "created_at": value2.created_at,
                "updated_at": value2.updated_at,
            }
                for value2 in product_category]
        })
        # print(data)
        return data


class getProductByCategoryView(View):
    def get_data(self, pk):
        print(pk)
        data = {}
        product_by_category = Product.objects.filter(product_category_id__id=pk)
        print(product_by_category)
        print(list(product_by_category))
        return list(product_by_category)


class getOneProductDetailsView(View):
    def get_data(self, pk):
        print(pk)
        data = {}
        product_detail = Product.objects.filter(id=pk)
        print(product_detail)
        print(list(product_detail))
        return list(product_detail)


# Templates rendering
# class ForgotPasswordView(View):
#
#     forgotPasswordForm_templates = 'dashboard/forgotPassword_form.html'
#     forgotMessageForm_templates = 'dashboard/password_reset_message.html'
#
#     def get(self, request, *args, **kwargs):
#         print(kwargs.get('pk'))
#         request.session['id'] = kwargs.get('pk')
#         # return render(request, self.forgotPasswordForm_templates)
#
#         try:
#             userInstance = User.objects.get(pk=int(kwargs.get('pk')))
#             registerUserInstance = RegisterUser.objects.get(user=userInstance, userId=int(kwargs.get('pk')))
#             request.session['id'] = kwargs.get('pk')
#             print(request.session['id'])
#             return render(request, self.forgotPasswordForm_templates)
#         except:
#             context = {"msg1": "invalid Username! ", "msg2": "User Not Exists!"}
#             return render(request, self.forgotMessageForm_templates, context)
#
#     def post(self, request, *args, **kwargs):
#         print(kwargs.get('pk'))
#         print(request.session['id'])
#         if request.method == "POST":
#             username = request.POST['username']
#             password1 = request.POST['password1']
#             password2 = request.POST['password2']
#
#             if password1 == password2:
#                 try:
#                     userInstance = User.objects.get(username=username)
#                     registerUserInstance = RegisterUser.objects.get(user=userInstance, userId=int(request.session['id']))
#                 except:
#                     print("error")
#                     context = {"msg1": "invalid Username! ", "msg2": "please Enter Correct User Name"}
#                     return render(request, self.forgotMessageForm_templates, context)
#
#                 if password2:
#
#                     msg = 'Note: password is as least 8 characters long and has at least 2 digits and 1 Upper case letter'
#                     min_length = 8
#
#                     if len(password2) < min_length:
#
#                         context = {"msg1": "invalid password! ", "msg2": 'Password must be at least {0} characters '
#                                                                      'long.'.format(min_length) + msg}
#                         return render(request, self.forgotMessageForm_templates, context)
#
#                     if len(password2) > 20:
#
#                         context = {"msg1": "invalid password! ", "msg2": 'Password not more then 20 characters '
#                                                                      'long.'.format(min_length) + msg}
#                         return render(request, self.forgotMessageForm_templates, context)
#
#                     # check for 2 digits
#                     if sum(c.isdigit() for c in password2) < 2:
#                         context = {"msg1": "invalid password! ", "msg2": 'Password must contain at least 2 digits.' + msg}
#                         return render(request, self.forgotMessageForm_templates, context)
#
#                     # check for uppercase letter
#                     if not any(c.isupper() for c in password2):
#                         context = {"msg1": "invalid password! ",
#                                    "msg2": 'Password must container at least 1 uppercase letter.' + msg}
#                         return render(request, self.forgotMessageForm_templates, context)
#
#                 else:
#                     context = {"msg1": "invalid Password! ", "msg2": "please Enter Passord"}
#                     return render(request, self.forgotMessageForm_templates, context)
#
#                 userInstance.set_password(password2)
#                 registerUserInstance.password = password2
#                 userInstance.save()
#                 registerUserInstance.save()
#
#                 context = {"msg1": "Password reset complete", "msg2": "Your password has been set. You may go ahead and log in now."}
#                 return render(request, self.forgotMessageForm_templates, context)
#             else:
#                 # print("password not same")
#                 context = {"msg1":"Password Must Match", "msg2":"Please Enter Valid Password"}
#                 return render(request, self.forgotMessageForm_templates, context)


class Dashboard(View):
    login_template = 'dashboard/login.html'
    dashboard_template = 'dashboard/index1.html'

    def get(self, request, *args, **kwargs):

        print(request.session.get('tokenId'))
        print(request.session.get('userData'))
        # if request.session.get('tokenId') is None:
        #     return redirect(to='VendorLogin')
        # else:
        return render(request, self.dashboard_template)

class ContactView(View):
    contact_template = 'dashboard/contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.contact_template)

    def post(self, request, *args, **kwargs):
        print("in post")
        return render(request, self.contact_template)

class AboutUsView(View):
    about_template = 'dashboard/about.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.about_template)

    def post(self, request, *args, **kwargs):
        print("in post")
        return render(request, self.about_template)


# from django.views.decorators.csrf import csrf_exempt

class Register(View):
    # register_template = 'dashboard/index1.html'
    register_template = 'dashboard/signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.register_template)

    def post(self, request, *args, **kwargs):

        url = 'https://ecomm-api-724sg5bjxa-de.a.run.app/mobile_api/CreateVendorManagement/'

        headers = {'Content-Type': 'application/json'},

        # payload = {
        #     'first_name': request.POST['first_name'],
        #     'last_name': request.POST['last_name'],
        #     'email': request.POST['email'],
        #     'mob_no': request.POST['mobile'],
        #     'password': request.POST['password1'],
        #     'password2': request.POST['password2'],
        # }

        payload = {
            'first_name': request.POST.get('First Name'),
            'last_name': request.POST.get('Last Name'),
            'email': request.POST.get('Email'),
            'mob_no': request.POST.get('phone'),
            'password': request.POST.get('password'),
            'password2': request.POST.get('Confirm Password'),
        }

        r = requests.post(url, data=payload)
        print(r.json())
        # print(r.status_code)
        stat = r.json().get("status")
        msg = r.json().get("message")
        print(stat)
        if stat == 'success' and msg == 'OK':
            return redirect(to='VendorLogin')
        else:
            print(msg)
            error_msg = msg.get("email")
            error_msg_pass = msg.get("password2")
            error_msg_mob_no = msg.get("mob_no")
            if error_msg:
                errorMessage = error_msg[0]
            elif error_msg_pass:
                errorMessage = error_msg_pass[0]
            elif error_msg_mob_no:
                errorMessage = error_msg_mob_no[0]
            else:
                errorMessage = "Something went wrong"

            context = {"messages": errorMessage, "errStatus": "something wrong"}
            return render(request, self.register_template, context)


class Login(View):
    login_template = 'dashboard/signIn.html'

    def get(self, request, *args, **kwargs):
        request.session['tokenId'] = None
        request.session['action'] = "loginNotSuccess"
        return render(request, self.login_template)

    def post(self, request, *args, **kwargs):

        url = 'https://ecomm-api-724sg5bjxa-de.a.run.app/mobile_api/api-token-auth/'

        headers = {'Content-Type': 'application/json'},

        payload = {
            'username': request.POST['Email'],
            'password': request.POST['password']
        }

        r = requests.post(url, data=payload)
        # print(r.text)
        print(r.json())
        # print(r.status_code)
        stat = r.json().get("status")
        msg = r.json().get("message")
        print(stat)
        if stat == 'success' and msg == 'OK':
            details = r.json().get("token")
            tokenId = details.get("token")
            userDetail = details.get("userDetails")
            userData = userDetail.get("user")
            userName = userData[0].get("userName")
            vendor_id = userData[0].get("vendor_id")
            vend_id = userData[0].get("id")
            print(userData[0])
            print(tokenId)
            request.session['tokenId'] = tokenId
            request.session['id'] = vend_id
            request.session['userName'] = userName
            request.session['vendor_id'] = vendor_id
            request.session['action'] = "loginSuccess"
            # return render(request, self.dashboard_template)
            return redirect(to='VendorDashboard')
        else:
            error_msg = msg.get("non_field_errors")
            if error_msg[0] == "Unable to log in with provided credentials.":
                errorMessage = error_msg[0]
            else:
                errorMessage = "Something Went Wrong !"
            print(error_msg[0])
            print(errorMessage)
            context = {"messages": errorMessage, "errStatus": "something wrong"}
            return render(request, self.login_template, context)


class AccountSetting(View):
    account_setting_template = 'dashboard/naviGation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.account_setting_template)


class ProductsView(View):
    from .forms import ProductForm
    products_template = 'dashboard/products.html'
    form = ProductForm
    model = Product

    def get(self, request, *args, **kwargs):
        print(request.session.get('tokenId'))
        print(request.session.get('userData'))
        if request.session.get('tokenId') is None:
            return redirect(to='VendorLogin')
        else:
            return render(request, self.products_template, {'form': self.form})

    def post(self, request, *args, **kwargs):
        print("okk")
        form = self.form(request.POST, request.FILES, )
        print(form.is_valid())
        # print(form)
        if form.is_valid():
            product_category_id = form.cleaned_data.get('product_category_id')
            product_name = form.cleaned_data.get('product_name')
            product_description = form.cleaned_data.get('product_description')
            product_images = form.cleaned_data.get('product_images')
            product_price = form.cleaned_data.get('product_price')
            product_status = form.cleaned_data.get('product_status')
            discount = form.cleaned_data.get('discount')
            rating = form.cleaned_data.get('rating')

            print(product_category_id)
            print(product_name)
            print(product_images)
            self.model.objects.create(
                product_category_id=product_category_id,
                product_name=product_name,
                product_description=product_description,
                product_images=product_images,
                product_price=product_price,
                product_status=product_status,
                discount=discount,
                rating=rating
            )
            return redirect(to="StockDetailsView")
        return redirect(to="VendorProductsView")


class ProductCategoryView(View):
    from .forms import ProductCategoryForm
    products_category_template = 'dashboard/productCategory.html'
    form = ProductCategoryForm
    model = Product_category

    def get(self, request, *args, **kwargs):
        print(request.session.get('tokenId'))
        print(request.session.get('userData'))
        if request.session.get('tokenId') is None:
            return redirect(to='VendorLogin')
        else:
            return render(request, self.products_category_template, {'form': self.form})

    def post(self, request, *args, **kwargs):
        print("okk")
        form = self.form(request.POST, request.FILES, )
        print(form.is_valid())
        # print(form)
        if form.is_valid():
            category_name = form.cleaned_data.get('category_name')
            category_description = form.cleaned_data.get('category_description')
            product_thumbnail = form.cleaned_data.get('product_thumbnail')

            self.model.objects.create(
                category_name=category_name,
                category_description=category_description,
                product_thumbnail=product_thumbnail,
            )
            return redirect(to="StockDetailsView")
        return redirect(to="VendorProductCategoryView")


class VendorStockView(View):
    # from .forms import ProductCategoryForm
    stock_template = 'dashboard/vendorStock.html'
    # form = ProductCategoryForm
    # model = Product_category

    def get(self, request, *args, **kwargs):
        print(request.session.get('tokenId'))
        print(request.session.get('userData'))
        if request.session.get('tokenId') is None:
            return redirect(to='VendorLogin')
        else:
            url = 'https://ecomm-api-724sg5bjxa-de.a.run.app/mobile_api/SelectProduct/'
            r = requests.post(url)
            print(r.json())
            stat = r.json().get("status")
            msg = r.json().get("message")
            print(stat)
            if stat == 'success' and msg == 'OK':
                products = r.json().get("data")

                url = 'https://ecomm-api-724sg5bjxa-de.a.run.app/mobile_api/SelectProductCatrgory/'
                r = requests.post(url)
                print(r.json())
                stat = r.json().get("status")
                msg = r.json().get("message")
                print(stat)
                if stat == 'success' and msg == 'OK':
                    categories = r.json().get("data")
                    context = {'products': products, 'categories':categories}
                    return render(request, self.stock_template, context)
                else:
                    return redirect(to='VendorDashboard')
            else:
                return redirect(to='VendorDashboard')

    def post(self, request, *args, **kwargs):
        url = 'https://ecomm-api-724sg5bjxa-de.a.run.app/mobile_api/VendorStockDetails/'

        payload = {
            'product_id': request.POST.get('product'),
            'product_category_id': request.POST.get('category'),
            'quantity': int(request.POST.get('quantity')),
            'price': float(request.POST.get('price')),
            'selling_price': float(request.POST.get('selling_price')),
            'status': bool(request.POST.get('status'))
        }

        r = requests.post(url, data=payload, headers={'Authorization': 'token ' + str(request.session.get('tokenId'))})
        # print(r.text)
        print(r.json())
        # print(r.status_code)
        stat = r.json().get("status")
        msg = r.json().get("message")
        print(stat)
        if stat == 'success' and msg == 'OK':
            return redirect(to='StockDetailsView')
        else:
            return redirect(to='VendorDashboard')

class StockDetailsView(View):
    from .vendorStockModel import Vendor_Stock
    model = Vendor_Stock
    stock_details_template = 'dashboard/stockDetails.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('tokenId') is None:
            return redirect(to='VendorLogin')
        else:
            url = 'https://ecomm-api-724sg5bjxa-de.a.run.app/mobile_api/GetOnlyVendorStockDetails/'

            print(request.session.get('vendor_id'))
            r = requests.get(url, headers={'Authorization': 'token ' + str(request.session.get('tokenId'))})
            # print(r.text)
            print(r.json())
            # print(r.status_code)
            stat = r.json().get("status")
            msg = r.json().get("message")
            print(stat)
            if stat == 'success' and msg == 'OK':
                data = r.json().get("data")
                print(data)
                context = {"data":data}
                return render(request, self.stock_details_template, context)

            else:
                return redirect(to='VendorVendorStockView')


class VendorStockUpdateDeleteView(View):
    # from .forms import ProductCategoryForm
    stock_template = 'dashboard/vendorStockUpdateDelete.html'
    # form = ProductCategoryForm
    # model = Product_category

    def get(self, request, *args, **kwargs):
        print(request.session.get('tokenId'))
        print(kwargs.get('pk'))
        pk_str = str(kwargs.get('pk'))
        url = 'http://127.0.0.1:8000/mobile_api/VendorStockDetails/'+pk_str+'/'
        r = requests.put(url, headers={'Authorization': 'token ' + str(request.session.get('tokenId'))})
        print(r.json())
        stat = r.json().get("status")
        msg = r.json().get("message")
        print(stat)
        if stat == 'success' and msg == 'OK':
            products = r.json().get("data")
            context = {""}
            return render(request, self.stock_template, context)

        else:
            return redirect(to='VendorDashboard')

class AddStoreDetails(View):
    add_stock_Address_template = 'dashboard/add_Store_details.html'
    register_address_template = 'dashboard/registerDetails.html'

    def get(self, request, *args, **kwargs):
        print(request.session.get('tokenId'))
        print(kwargs.get('pk'))
        if request.session.get('tokenId') is None:
            return redirect(to='VendorLogin')
        else:
            return render(request, self.add_stock_Address_template)

    def post(self, request, *args, **kwargs):
        print(request.session.get('tokenId'))
        print(request.session.get('id'))

        payload = {
            'address1': request.POST.get('address1'),
            'address2': request.POST.get('address2'),
            'pincode': int(request.POST.get('pincode')),
            'notes': request.POST.get('notes'),
            'id_proof': request.POST.get('id_proof'),
        }

        url = 'https://ecomm-api-724sg5bjxa-de.a.run.app/mobile_api/VendorManagementDetails/'+str(request.session.get('id'))+'/'
        print(url)
        r = requests.put(url, data=payload, headers={'Authorization': 'token ' + str(request.session.get('tokenId'))})
        print(r.json())
        stat = r.json().get("status")
        msg = r.json().get("message")
        print(stat)
        if stat == 'success' and msg == 'OK':
            data = r.json().get("data")
            print(data)
            # context = {"data": data}
            # return render(request, self.register_address_template, context)
            return redirect(to='GetRegisterDetails')
        else:
            return render(request, self.add_stock_Address_template)

class GetRegisterDetails(View):
    print("in register")
    register_address_template1 = 'dashboard/registerDetails.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('tokenId') is None:
            return redirect(to='VendorLogin')
        else:

            url = 'https://ecomm-api-724sg5bjxa-de.a.run.app/mobile_api/VendorManagementDetails/'+str(request.session.get('id'))+'/'
            print(url)
            r = requests.get(url, headers={'Authorization': 'token ' + str(request.session.get('tokenId'))})
            print(r.json())
            stat = r.json().get("status")
            msg = r.json().get("message")
            print(stat)
            if stat == 'success' and msg == 'OK':
                data = r.json().get("data")
                print(data)
                context = {"data": data}
                return render(request, self.register_address_template1, context)
            else:
                return redirect(to='VendorDashboard')

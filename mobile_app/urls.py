from django.urls import path
from .views import ProductDetail, CreateSuperUserRegister
from .views import AppToken, UserAPI,CreateUserRegister, OrderDetail, OrderHistory, Product_image_uplod_View, OrderActionDetail, \
    ShippingAddress, OfferDetails, Offer_Apply, DeliveryBoyData, CreateVendorManagement, VendorManagementDetails, VendorStockDetails,\
    ProductCategoryDetails, productDetailsView, ProductSearchAPI, HomePageContentAPI, GetProductByCategory, GetOneProductDetailsAPI, \
    UserRegisterDetails, UserProfileImageUpload, ChangePasswordView, ValidatePhoneSendOTP, ValidateOTP, ProductSubscribe,\
    SelectProductCatrgory, SelectProduct, placeOrderView, EmaiId_Mobile_no_Verification, ForgotPasswordView, AddUserEmail, \
    ProductSubscribeStopeAndResume, CreateUserRegisterFB, ForgotPasswordResetView, GetOnlyVendorStockDetails
    #, ForgotPasswordView


urlpatterns = [
    path('api-token-auth/', AppToken.as_view()),
    path('UserAPI/', UserAPI.as_view()),

    path('CreateUserRegister/', CreateUserRegister.as_view()),
    path('CreateUserRegisterFB/', CreateUserRegisterFB.as_view()),
    path('CreateSuperUserRegister/', CreateSuperUserRegister.as_view()),
    path('CreateVendorManagement/', CreateVendorManagement.as_view()),
    path('ValidatePhoneSendOTP/', ValidatePhoneSendOTP.as_view()),
    path('ValidateOTP/', ValidateOTP.as_view()),
    path('EmaiId_Mobile_no_Verification/', EmaiId_Mobile_no_Verification.as_view()),

    path('UserRegisterDetails/', UserRegisterDetails.as_view()),

    path('UserRegisterDetails/<str:pk>/', UserRegisterDetails.as_view()),

    path('UserProfileImageUpload/', UserProfileImageUpload.as_view()),

    path('product/', ProductDetail.as_view()),

    path('product/<str:pk>/', ProductDetail.as_view()),

    path('order/', OrderDetail.as_view()),

    path('order/<str:pk>/', OrderDetail.as_view()),

    # path('orderHistory/', OrderHistory.as_view()),

    # path('orderHistory/<str:pk>/', OrderHistory.as_view()),

    path('ProductImageUplod/', Product_image_uplod_View.as_view()),

    path('OrderActionDetail/', OrderActionDetail.as_view()),

    path('ShippingAddress/', ShippingAddress.as_view()),

    path('ShippingAddress/<str:pk>/', ShippingAddress.as_view()),

    path('OfferDetails/', OfferDetails.as_view()),

    path('OfferDetails/<str:pk>/', OfferDetails.as_view()),

    path('Offer_Apply/', Offer_Apply.as_view()),

    path('DeliveryBoyData/', DeliveryBoyData.as_view()),

    path('DeliveryBoyData/<str:pk>/', DeliveryBoyData.as_view()),

    path('VendorManagementDetails/', VendorManagementDetails.as_view()),

    path('VendorManagementDetails/<str:pk>/', VendorManagementDetails.as_view()),

    path('VendorStockDetails/<str:pk>/', VendorStockDetails.as_view()),

    path('VendorStockDetails/', VendorStockDetails.as_view()),

    path('ProductCategoryDetails/', ProductCategoryDetails.as_view()),

    path('ProductCategoryDetails/<str:pk>/', ProductCategoryDetails.as_view()),
    path('SelectProductCatrgory/', SelectProductCatrgory.as_view()),

    path('productDetailsView/', productDetailsView.as_view()),
    path('SelectProduct/', SelectProduct.as_view()),

    path('productDetailsView/<str:pk>/', productDetailsView.as_view()),

    path('ProductSubscribe/', ProductSubscribe.as_view()),
    path('ProductSubscribe/<str:pk>/', ProductSubscribe.as_view()),

    path('ProductSubscribeStopeAndResume/<str:pk>/', ProductSubscribeStopeAndResume.as_view()),

    path('ProductSearchAPI/', ProductSearchAPI.as_view()),

    path('HomePageContentAPI/', HomePageContentAPI.as_view()),

    path('HomePageContentAPI/<str:pk>/', HomePageContentAPI.as_view()),

    path('GetProductByCategory/<str:pk>/', GetProductByCategory.as_view()),

    path('GetOneProductDetailsAPI/<str:pk>/', GetOneProductDetailsAPI.as_view()),

    path('ChangePasswordView/', ChangePasswordView.as_view()),

    path('AddUserEmail/', AddUserEmail.as_view()),

    path('ForgotPasswordView/', ForgotPasswordView.as_view()),

    path('placeOrderView/', placeOrderView.as_view()),


    path('ForgotPasswordResetView/', ForgotPasswordResetView.as_view()),


    path('GetOnlyVendorStockDetails/', GetOnlyVendorStockDetails.as_view()),

]
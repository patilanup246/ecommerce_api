from django.urls import path
# from .views import ForgotPasswordView
from .views import Dashboard, Register, Login, AccountSetting, ProductsView, ProductCategoryView, VendorStockView, ContactView, \
    AboutUsView, StockDetailsView, AddStoreDetails, GetRegisterDetails, VendorStockUpdateDeleteView

urlpatterns = [
    # path('ForgotPasswordView/<str:pk>/', ForgotPasswordView.as_view(), name='ForgotPasswordView'),
    # path('ForgotPasswordView/<str:pk>/', ForgotPasswordView.as_view()),
    path('VendorDashboard/', Dashboard.as_view(), name='VendorDashboard'),
    path('VendorRegister/', Register.as_view(), name='VendorRegister'),
    path('VendorLogin/', Login.as_view(), name='VendorLogin'),
    path('VendorAccountSetting/', AccountSetting.as_view(), name='VendorAccountSetting'),
    path('VendorProductsView/', ProductsView.as_view(), name='VendorProductsView'),
    path('VendorProductCategoryView/', ProductCategoryView.as_view(), name='VendorProductCategoryView'),
    path('VendorVendorStockView/', VendorStockView.as_view(), name='VendorVendorStockView'),
    path('ContactView/', ContactView.as_view(), name='ContactView'),
    path('AboutUsView/', AboutUsView.as_view(), name='AboutUsView'),
    path('StockDetailsView/', StockDetailsView.as_view(), name='StockDetailsView'),
    path('VendorStockUpdateDeleteView/<str:pk>/', VendorStockUpdateDeleteView.as_view(), name='VendorStockUpdateDeleteView'),

    path('AddStoreDetails/', AddStoreDetails.as_view(), name='AddStoreDetails'),
    path('GetRegisterDetails/', GetRegisterDetails.as_view(), name='GetRegisterDetails'),
    ]
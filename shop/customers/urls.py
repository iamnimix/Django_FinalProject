from django.urls import path
from . import api
from . import views

app_name = 'customers'

urlpatterns = [
      path('edit/profile/', views.show_profile, name='edit_profile'),
      path('load/', views.ProfileInfo.as_view(), name='load'),
      path('profile/', api.Profile.as_view(), name='profile'),
      path('api/login/', api.LoginAPIView.as_view(), name='login'),
      path('login-simple/', views.LoginSimple.as_view(), name='login_simple'),
      path('login-otp/', api.LoginOtp.as_view(), name='login_otp'),
      path('verification/', api.Verification.as_view(), name='verification'),
      path('api/register/', api.RegisterApi.as_view(), name="register"),
      path('logout/', api.Logout.as_view(), name='logout'),
      path('address/', api.AddressApi.as_view(), name='address'),
      path('address-info/', views.AddressInfo.as_view(), name='address_info'),
      path('order/', api.OrderAPI.as_view(), name='order'),
      path('order-info/', views.OrderInfo.as_view(), name='order_info'),
      path('order/<int:pk>/', api.OrderDetail.as_view(), name='order_detail'),
      path('order-detail/', views.OrderDetailInfo.as_view(), name='order_detail_info'),
]

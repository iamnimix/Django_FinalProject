from django.urls import path
from . import api
from . import views

app_name = 'customers'

urlpatterns = [
      path('api/login/', api.LoginAPIView.as_view(), name='login'),
      path('register/', views.RegisterView.as_view(), name="sign_up"),
      path('api/register/', api.RegisterApi.as_view(), name="register"),
]

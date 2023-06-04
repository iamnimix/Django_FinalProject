from django.urls import path
from . import api
from . import views

app_name = 'customers'

urlpatterns = [
      path('edit/profile/', views.Profile.as_view(), name='edit_profile'),
      path('profile/', api.Profile.as_view(), name='profile'),
      path('api/login/', api.LoginAPIView.as_view(), name='login'),
      path('api/register/', api.RegisterApi.as_view(), name="register"),
      path('logout/', api.Logout.as_view(), name='logout')
]

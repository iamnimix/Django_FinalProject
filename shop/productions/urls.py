from django.urls import path
from . import views
app_name = 'productions'

urlpatterns = [
    path('', views.main_page),
    path('<int:id>/', views.detail_page, name='detail'),
]

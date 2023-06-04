from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.show_cart, name='cart'),
    path('detail/', views.CartDetail.as_view(), name='cart_api'),
    path('add/<int:product_id>/', views.AddCartItemView.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', views.CartRemoveItemView.as_view(), name='cart_remove'),
]

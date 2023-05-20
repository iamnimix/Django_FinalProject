from django.urls import path
from . import views
app_name = 'productions'

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path("<slug:category_slug>/", views.ProductList.as_view(), name="product_list_by_category"),
    path('<int:id>/', views.detail_page, name='detail'),
]

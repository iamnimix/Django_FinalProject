from django.urls import path, re_path
from . import views
app_name = 'productions'

urlpatterns = [
    path('', views.LandingPage.as_view(), name='landing_page'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path("<slug:category_slug>/", views.ProductList.as_view(), name="product_list_by_category"),
    path('<int:id>/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
]

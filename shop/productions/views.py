from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from .models import Product, Image, Category


# Create your views here.

class LandingPage(View):
    def get(self, request):
        last_5_products = Product.objects.order_by('-id')[:5]
        return render(request, "landing_page.html", {'products': last_5_products})


class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 4


class ProductList(ListView):
    model = Product
    template_name = 'list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['object_list']:
            product.price = '{:20,.0f}'.format(product.price)
        context['categories'] = Category.objects.all()

        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('id')
        context['images'] = Image.objects.filter(product_id=product_id)
        context['product'].price = '{:20,.0f}'.format(context['product'].price)
        return context

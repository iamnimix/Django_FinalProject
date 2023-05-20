from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView

from .models import Product, Image, Category


# Create your views here.

class ProductList(ListView):
    model = Product
    template_name = 'list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            # Filter products by category
            category = Category.objects.get(slug=category_slug)
            queryset = queryset.filter(category=category)

        return queryset


def detail_page(request, id):
    product = Product.objects.get(id=id)
    images = Image.objects.filter(product_id=id)
    return render(request, 'detail.html', context={'product': product, "images": images})

from django.shortcuts import render
from .models import Product, Image


# Create your views here.

def main_page(request):
    products = Product.objects.all()
    return render(request, 'list.html', context={'products': products})


def detail_page(request, id):
    product = Product.objects.get(id=id)
    images = Image.objects.filter(product_id=id)
    return render(request, 'detail.html', context={'product': product, "images": images})

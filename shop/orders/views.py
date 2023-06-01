from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import CartAddProductForm
from productions.models import Product
from .models import Cart
from .serializer import CartSerializer, OrderItemSerializer
from django.conf import settings


# Create your views here.


class AddCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        cart_tuple = Cart.objects.get_or_create(user=request.user)
        cart = cart_tuple[0]
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add_item(product, quantity)
            cart_serializer = CartSerializer(cart, many=True)
            cart_serializer.save()
            response = Response(cart_serializer.data, status=status.HTTP_200_OK)
            response.set_cookie(settings.CART_COOKIE_NAME, cart_serializer.data)
            return response


class CartDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


def show_cart(request):
    return render(request, 'cart.html', {})

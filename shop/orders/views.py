import uuid

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import CartAddProductForm
from productions.models import Product
from .models import Cart, OrderItem
from .serializer import CartSerializer, OrderItemSerializer
from django.conf import settings


# Create your views here.


class AddCartItemView(APIView):

    def post(self, request, product_id):
        cart_identifier = request.COOKIES.get('cart_identifier')
        if not cart_identifier:
            cart_identifier = str(uuid.uuid4())
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        cart_tuple = Cart.objects.get_or_create(identifier=cart_identifier)
        cart = cart_tuple[0]
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add_item(product, quantity)
            cart_serializer = CartSerializer(cart)
            response = Response(cart_serializer.data, status=status.HTTP_200_OK)
            response.set_cookie(settings.CART_COOKIE_NAME, cart_serializer.data)
            response.set_cookie('cart_identifier', cart_identifier)
            return response


class CartRemoveItemView(APIView):

    def post(self, request, product_id):
        cart_identifier = request.COOKIES.get('cart_identifier')
        if not cart_identifier:
            cart_identifier = str(uuid.uuid4())
        cart = Cart.objects.get_or_create(identifier=cart_identifier)
        cart = cart[0]
        product = get_object_or_404(Product, id=product_id)
        cart.remove_item(product)
        response = Response(status=200)
        response.set_cookie(settings.CART_COOKIE_NAME, '')
        return response


class CartDetail(APIView):

    def get(self, request):
        cart_identifier = request.COOKIES.get('cart_identifier')
        if not cart_identifier:
            cart_identifier = str(uuid.uuid4())
        cart, _ = Cart.objects.get_or_create(identifier=cart_identifier)
        serializer = CartSerializer(cart)
        response = Response(serializer.data)
        response.set_cookie('cart_identifier', cart_identifier)
        return response


def show_cart(request):
    return render(request, 'cart.html', {})

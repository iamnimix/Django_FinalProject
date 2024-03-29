import uuid

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import CartAddProductForm, OrderForm
from productions.models import Product
from .models import Cart, OrderItem, Order, Address
from .serializer import CartSerializer, OrderItemSerializer, OrderDetailSerializer
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
    """
        Detail of Cart
    """

    serializer_class = CartSerializer

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


# SHOW CHECKOUT HTML
def show_checkout(request):
    if request.user.is_authenticated:
        form = OrderForm(request.POST or None, user=request.user)
        return render(request, 'checkout.html', {'form': form})
    else:
        return HttpResponse('ابتدا وارد شوید')


#  ADD ORDER in DATABASE
class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        address_id = request.data.get('address')
        address = Address.objects.get(pk=address_id)
        order = Order.objects.create(address_id=address, user_id=request.user)
        serializer = OrderDetailSerializer(order)
        cart_identifier = request.COOKIES.get('cart_identifier')
        cart = Cart.objects.get(identifier=cart_identifier)
        order_items = OrderItem.objects.filter(cart=cart)
        for item in order_items:
            item.order = order
            item.save()
        response = Response(serializer.data)
        response.delete_cookie('mycart')
        response.delete_cookie('cart_identifier')
        return response


# PAID ORDER
class CheckOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = Order.objects.filter(user_id=request.user).order_by('id').last()
        order.paid = True
        order.save()
        return Response()


class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)


class OrderDetailInfo(APIView):
    def get(self, request):
        html = render(request, 'order_detail.html')
        return Response({'html': html.content})

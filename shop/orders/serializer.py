from rest_framework import serializers
from .models import Cart, OrderItem
from productions.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'main_image']


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'quantity', 'price']


class CartSerializer(serializers.ModelSerializer):
    cartitem_set = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cartitem_set']

    def get_cartitem_set(self, cart):
        cart_items = OrderItem.objects.filter(cart=cart)
        serializer = OrderItemSerializer(cart_items, many=True)
        return serializer.data

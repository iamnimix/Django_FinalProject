from rest_framework import serializers
from .models import User
from orders.models import Address, Order


class OrderSerializer(serializers.ModelSerializer):
    jalali_date = serializers.SerializerMethodField()

    def get_jalali_date(self, obj):
        return obj.get_jalali_date()

    class Meta:
        model = Order
        fields = ['id', 'created', 'jalali_date']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['state', 'city', 'street']


class UserSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(phone=validated_data['phone'], email=validated_data['email'],
                                   fullname=validated_data['fullname'])
        user.set_password(validated_data['password1'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'email', 'fullname']

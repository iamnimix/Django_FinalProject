from rest_framework import serializers
from .models import User


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


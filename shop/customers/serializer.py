from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["phone", "password"]

    def create(self, validated_data):
        user = User.objects.create(phone=validated_data['phone'])
        user.set_password(validated_data['password'])
        user.save()
        return user


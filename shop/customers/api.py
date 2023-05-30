import jwt
from django.http import HttpResponse, QueryDict, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer, UserProfileSerializer
from .forms import CustomUserCreationForm
from .models import User
from django.conf import settings


class RegisterApi(APIView):

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                serializer = UserSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)

        else:
            errors = form.errors
            return Response(errors)


class LoginAPIView(APIView):
    def get(self, request):
        return render(request, 'login.html')


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_object(self, pk):
        user = get_object_or_404(User, pk=pk)
        return user

    def put(self, request):
        # query_params = QueryDict(request.META['QUERY_STRING'])
        # user_id = query_params.get('userId')
        access_token = request.COOKIES.get('access_token')
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        user = self.get_user_object(user_id)
        serializer = UserProfileSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Logout(APIView):
    def post(self, request):
        response = JsonResponse({'message': 'Logout successful.'})
        response.delete_cookie('access_token')
        return response

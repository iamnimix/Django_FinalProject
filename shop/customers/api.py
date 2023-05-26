from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer
from .forms import CustomUserCreationForm


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

    def post(self, request):
        if request.POST.get("logout"):
            logout(request)
            return redirect("login")
        phone = request.POST['phone']
        password = request.POST['password']

        # Validate the user's credentials
        user = authenticate(phone=phone, password=password)
        if user is None:
            # If the credentials are not valid, return an error response
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            login(request, user)
            return redirect("productions:landing_page")

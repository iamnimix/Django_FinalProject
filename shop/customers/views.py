import jwt
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from django.conf import settings


def show_profile(request):
    return render(request, 'profile.html', context={})


class ProfileInfo(APIView):
    def get(self, request):
        html = render(request, 'edit_prof.html')
        return Response({'html': html.content})


class AddressInfo(APIView):
    def get(self, request):
        html = render(request, 'address.html')
        return Response({'html': html.content})


class OrderInfo(APIView):
    def get(self, request):
        html = render(request, 'order.html')
        return Response({'html': html.content})

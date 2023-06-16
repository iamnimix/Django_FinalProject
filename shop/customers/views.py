import jwt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from django.conf import settings


class LoginSimple(APIView):
    def get(self, request):
        html = render(request, 'login_simple.html')
        return Response({'html': html.content})


def show_profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', context={})
    else:
        return HttpResponse('ابتدا وارد شوید')


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


class OrderDetailInfo(APIView):
    def get(self, request):
        html = render(request, 'order_detail.html')
        return Response({'html': html.content})

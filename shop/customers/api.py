import jwt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, QueryDict, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import UserSerializer, UserProfileSerializer, AddressSerializer, OrderSerializer
from .models import User
from django.conf import settings
from orders.models import Cart, Address, Order
from orders.serializer import OrderDetailSerializer
from .tasks import send_otp_sms
import redis
from rest_framework import generics


class RegisterApi(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        return render(request, 'register.html', {})


class LoginAPIView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(phone=request.POST['phone'], password=request.POST['password'])
        login(request, user)
        return Response()


class LoginOtp(APIView):
    def get(self, request):
        html = render(request, 'login_otp.html')
        return Response({'html': html.content})

    def post(self, request):
        try:
            user = User.objects.get(phone=request.POST['phone'])
            response = Response()
            response.set_cookie('user_phone', user.phone)
            send_otp_sms.delay(user.phone)
            return response
        except User.DoesNotExist:
            pass


class Verification(APIView):
    def get(self, request):
        return render(request, 'verification.html')

    def post(self, request):
        otp = int(request.POST['code'])
        print(otp)
        r = redis.Redis(host='redis', port=6379, db=0)
        code = int(r.get(request.COOKIES.get('user_phone')))
        print(type(code))
        if code == otp:
            return Response({
                'status': 'success'
            }, status=status.HTTP_200_OK)
        else:
            print('else')
            return Response({
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def post(self, request):
        response = JsonResponse({'message': 'Logout successful.'})
        identifier_ = request.COOKIES.get('cart_identifier')
        try:
            cart = Cart.objects.get(identifier=identifier_)
            cart.delete()
        except:
            pass
        logout(request)
        response.delete_cookie('access_token')
        response.delete_cookie(settings.CART_COOKIE_NAME)
        return response


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            try:
                decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token.get('user_id')
                user = User.objects.get(pk=user_id)
                serializer = UserSerializer(user)
            except jwt.ExpiredSignatureError:
                response = Response({'error': 'Access token has expired'}, status=401)
                response.delete_cookie('access_token')
                return response
            except (jwt.DecodeError, jwt.InvalidTokenError):
                return Response({'error': 'Invalid access token'}, status=401)
            return Response(serializer.data)
        else:
            return Response({'error': 'Access token not found'}, status=401)

    def get_user_object(self, pk):
        user = get_object_or_404(User, pk=pk)
        return user

    def put(self, request):
        access_token = request.COOKIES.get('access_token')
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        user = self.get_user_object(user_id)
        serializer = UserProfileSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AddressApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user_id=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user_id'] = request.user
        serializer.save()
        return Response(serializer.data)


class OrderAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user_id=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

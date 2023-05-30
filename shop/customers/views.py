import jwt
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import User
from django.conf import settings


class RegisterView(TemplateView):
    template_name = 'register.html'


class Profile(View):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            try:
                decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token.get('user_id')
                user = User.objects.get(pk=user_id)
                return render(request, 'profile.html', context={'user': user})
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Access token has expired'}, status=401)
            except (jwt.DecodeError, jwt.InvalidTokenError):
                return JsonResponse({'error': 'Invalid access token'}, status=401)
        else:
            return JsonResponse({'error': 'Access token not found'}, status=401)

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

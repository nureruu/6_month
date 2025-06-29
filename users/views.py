from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ConfirmCodeSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView 
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_201_CREATED)

class ConfirmCodeView(generics.GenericAPIView):
    serializer_class = ConfirmCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Пользователь успешно подтвержден"}, status=200)
        return Response(serializer.errors, status=400)
class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

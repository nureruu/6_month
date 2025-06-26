from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ConfirmCodeSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class ConfirmCodeView(generics.GenericAPIView):
    serializer_class = ConfirmCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Пользователь успешно подтвержден"}, status=200)
        return Response(serializer.errors, status=400)

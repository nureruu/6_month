from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ConfirmationCode
from django.contrib.auth.models import User
from users.models import CustomUser
User = get_user_model()

class User_Base_Serializers(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        ConfirmationCode.objects.create(user=user)
        return user


class ConfirmCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        username = data['username']
        code = data['code']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        if not hasattr(user, 'confirmation') or user.confirmation.code != code:
            raise serializers.ValidationError("Неверный код подтверждения")

        data['user'] = user
        return data

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.is_active = True
        user.save()
        user.confirmation.delete()
        return user

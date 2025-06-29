from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ConfirmationCode
from django.contrib.auth.models import User
from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import date

User = get_user_model()

class User_Base_Serializers(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

class AuthValidateSerializer(serializers.Serializer):
    pass
class RegisterSerializer(serializers.ModelSerializer):
    def validate_username(self, username):
        try:
            CustomUser.objects.get(username=username)
        except:
            return username
        raise ValueError('user already exist!')
class ConfirmCodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField()

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        code = attrs.get('code')

        try:
            user = CustomUser.objects.get(id = user_id)
        except CustomUser.DoesNotExist:
            raise ValueError('user alr exist!')
        try:
            confirmation_code = ConfirmationCode.objects.get(user = user)
        except ConfirmationCode.DoesNotExist:
            raise ValueError('doesnt found!')
        if confirmation_code.code != code:
            raise ValueError('mistake')
        
        return attrs
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if user.birth_date is None:
            raise serializers.ValidationError("Пожалуйста, укажите дату рождения в профиле.")

        today = date.today()
        age = today.year - user.birth_date.year - (
            (today.month, today.day) < (user.birth_date.month, user.birth_date.day)
        )

        if age < 18:
            raise serializers.ValidationError("Вам должно быть не менее 18 лет для входа.")
        data['birth_date'] = str(user.birth_date)

        return data
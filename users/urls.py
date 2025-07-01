from django.urls import path
from .views import RegisterView, ConfirmCodeView, CustomTokenView, ConfirmView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token
from users .oauth import GoogleLoginView
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('confirm/', ConfirmCodeView.as_view()),
    path('login/', CustomTokenView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('api/v1/auth-token/', obtain_auth_token, name='api_token_auth'),
    path('google-login/', GoogleLoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("confirm/", ConfirmView.as_view()),
    
]

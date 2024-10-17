from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView
from django.contrib.auth.views import PasswordResetView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    
)
from .views import login, register
urlpatterns = [
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),


]

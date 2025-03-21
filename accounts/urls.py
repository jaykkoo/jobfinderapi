from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView
from django.contrib.auth.views import PasswordResetView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from .views import login, register, Account, logout, CheckAuthView
from .customrefreshtoken import RefreshTokenView
urlpatterns = [
    path('logout/', logout, name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('user/', Account.as_view(), name='user'),
    path('login/', login, name='login'),
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
]

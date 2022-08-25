from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterUserAPIView,
    VerifyEmail
)


urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('refresh', TokenRefreshView.as_view()),
    path('register', RegisterUserAPIView.as_view()),
    path('active', VerifyEmail.as_view()),
]

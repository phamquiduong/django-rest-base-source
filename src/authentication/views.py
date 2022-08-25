from rest_framework import generics
from .serializers import RegisterSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

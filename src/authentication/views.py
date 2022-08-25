from rest_framework import generics, views
from .serializers import RegisterSerializer, EmailVerificationSerializer
from core.helper.jwt_helper import jwt_decode
from django.shortcuts import render
from DB.models import User


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token', '')

        decode = jwt_decode(token)

        if 'errors' in decode:
            return render(request, 'auth/fail.html', {'message': decode['errors']})
        else:
            payload = decode.get('payload', {})
            user_id = payload.get('user_id', 0)

            try:
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()
            except Exception as e:
                return render(request, 'auth/fail.html', {'message': str(e)})

            return render(request, 'auth/success.html')

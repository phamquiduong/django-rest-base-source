from rest_framework import generics, views
from .serializers import RegisterSerializer, EmailVerificationSerializer, ForgotPasswordSerializer
from core.helper.jwt_helper import jwt_decode
# from django.shortcuts import render
from DB.models import User
from rest_framework.response import Response
from rest_framework.exceptions import status


class RegisterUserAPIView(generics.CreateAPIView):
    'Register new user return user common information'
    serializer_class = RegisterSerializer


class VerifyEmail(views.APIView):
    'Active your account get method with token in email inbox'
    serializer_class = EmailVerificationSerializer

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token', '')

        decode = jwt_decode(token)

        if 'errors' in decode:
            return Response({'details': decode['errors']}, status=status.HTTP_401_UNAUTHORIZED)
            # return render(request, 'auth/fail.html', {'message': decode['errors']})
        else:
            payload = decode.get('payload', {})
            user_id = payload.get('user_id', 0)

            try:
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()
            except Exception as e:
                return Response({'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
                # return render(request, 'auth/fail.html', {'message': str(e)})

            return Response({'details': 'Active account successfully'}, status=status.HTTP_200_OK)
            # return render(request, 'auth/success.html')


class ForgotPassword(views.APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        pass

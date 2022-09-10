import os
from datetime import timedelta
from rest_framework import serializers
from DB.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.conf import settings
from rest_framework.validators import UniqueValidator
from core.helper.jwt_helper import jwt_encode
from django.core.mail import EmailMessage


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, validators=[
                                     UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        if not validated_data.get('username', None):
            username = 'user_' + timezone.now().strftime('%Y%m%d%H%M%S%f')

        user = User.objects.create(
            username=username,
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        if not settings.EMAIL_OTP:
            user.is_active = True
            user.save()
        else:
            token = jwt_encode({
                'user_id': user.id,
                'exp': timezone.now() + timedelta(minutes=int(os.getenv('EMAIL_OTP_LIFETIME_MINUTE')))
            })
            email = EmailMessage(
                subject=os.getenv('EMAIL_SUBJECT'),
                body=os.getenv('EMAIL_MESSAGE').format(token=token),
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )
            email.content_subtype = "html"
            email.send()

        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        fields = ['token']


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

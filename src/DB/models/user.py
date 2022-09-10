from django.contrib.auth.models import AbstractUser
from django.db import models


class Group(models.Model):
    title = models.CharField(max_length=255, unique=True)


class User(AbstractUser):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email

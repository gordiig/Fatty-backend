from django.db import models
from django.contrib.postgres.fields import CIEmailField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Юзер
    """
    email = CIEmailField(null=False, blank=True, default='', unique=True)

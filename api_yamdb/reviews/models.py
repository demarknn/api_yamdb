import random
from django.conf import settings 
from django.contrib.auth.models import (
	AbstractUser, BaseUserManager, PermissionsMixin
)
from django.core.mail import send_mail
from django.db import models


class UserManager(BaseUserManager):
 
    def create_user(self, username, email):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')
        confirmation_code = str(random.randint(1000,9999))
        user = self.model(username=username, email=self.normalize_email(email), confirmation_code=confirmation_code)
        user.set_unusable_password()
        user.save()
        send_mail(
            username,
            confirmation_code,
            'from@yamdb.ru', 
            [email],
        ) 
        return user



class User(AbstractUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('a', 'User'),
        ('b', 'Moderator'),
        ('c', 'Admin'),
    )

    role = models.CharField(max_length=11, choices=ROLE_CHOICES, default='a')

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.username



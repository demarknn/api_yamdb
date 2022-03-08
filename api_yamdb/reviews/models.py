import random
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


ROLE_CHOICES = (
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
)


class UserManager(BaseUserManager):

    def create_user(
            self, username, email, password=None, role=None, bio=None):
        confirmation_code = str(random.randint(1000, 9999))
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            confirmation_code=confirmation_code
        )
        if role == 'admin':
            user.is_superuser = True
        if role == 'moderator':
            user.is_staff = True
        user.role
        user.set_password(password)
        user.bio
        user.save()
        send_mail(
            username,
            confirmation_code,
            'from@yamdb.ru',
            [email],
        )
        return user

    def create_superuser(
            self, username, email, password=None, role=None, bio=None):
        confirmation_code = str(random.randint(1000, 9999))
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            confirmation_code=confirmation_code
        )
        user.role
        user.set_password(password)
        user.bio
        user.is_superuser = True
        user.save()
        send_mail(
            username,
            confirmation_code,
            'from@yamdb.ru',
            [email],
        )
        return user


class User(AbstractUser, PermissionsMixin):
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='user'
    )
    password = models.CharField(max_length=200, default='password')
    bio = models.TextField(blank=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=10, default='0000')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return self.username


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Категория', max_length=256, unique=True)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Жанр', max_length=256, unique=True)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class Title(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Жанр', max_length=256, unique=True)
    year = models.IntegerField('Год выхода')
    description = models.CharField(
        'Описание', max_length=512, blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        null=True,
        related_name='genres'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category'
    )


class Reviews(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'], name='uniq')
        ]

    def __str__(self):
        return self.text[:15]


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:15]

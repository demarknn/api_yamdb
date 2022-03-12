from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class UserRole:
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]


class UserManager(BaseUserManager):

    def create_user(
            self, username, email, password=None, role=None, bio=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        if role == UserRole.MODERATOR:
            user.is_staff = True
        if role == UserRole.ADMIN:
            user.is_superuser = True
        user.role
        user.set_password(password)
        user.bio
        user.save()
        return user

    def create_superuser(
            self, username, email, password=None, role=None, bio=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.role
        user.set_password(password)
        user.bio
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser, PermissionsMixin):
    role = models.CharField(
        max_length=20, choices=UserRole.ROLE_CHOICES,
        default=UserRole.USER, verbose_name='Роль'
    )
    password = models.CharField(
        max_length=200,
        default='password',
        verbose_name='Пароль'
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Имя'
    )
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    confirmation_code = models.CharField(
        max_length=20,
        default='0000',
        verbose_name='Код подтверждения'
    )
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Категория', max_length=256, unique=True)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.name)


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Жанр', max_length=256, unique=True)
    slug = models.SlugField('Slug', max_length=50, unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.name)


class Title(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Жанр', max_length=256, unique=True)
    year = models.IntegerField('Год выхода', null=True)
    description = models.CharField(
        'Описание', max_length=512, blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='genres'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category'
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.IntegerField(
        'оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'], name='uniq')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text

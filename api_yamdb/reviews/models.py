from django.db import models


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
    description = models.CharField('Описание', max_length=512, blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='genres'
    )
    Category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category'
    )


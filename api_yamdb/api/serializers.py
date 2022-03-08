import re
import datetime as dt
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comments, Reviews, User, Genre, Category, Title


class ReviewsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Reviews
        read_only_field = ('title')
        validators = [
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(),
                fields=('title', 'author')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_field = ('review')


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if 'me' == value.lower():
            raise serializers.ValidationError(
                "Нельзя создавать пользователя ME"
            )
        if value == '':
            raise serializers.ValidationError("Нужно все заполнить")
        return value

    def validate_email(self, value):
        if value == '':
            raise serializers.ValidationError("Нужно все заполнить")
        return value


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
    
    def validate_slug(self, value):
        if (re.match('^[-a-zA-Z0-9_]+$', value) is not None
            and len(value) < 51):
            return value
        raise serializers.ValidationError(
            "Slug should contain only azAZ or numbers and 50 length"
        )


    def validate_name(self, value):
        if len(value) < 257:
            return value
        raise serializers.ValidationError(
            "Name should be 256 length"
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate_slug(self, value):
        if (re.match('^[-a-zA-Z0-9_]+$', value) is not None
            and len(value) < 51):
            return value
        raise serializers.ValidationError(
            "Slug should contain only azAZ or numbers and 50 length"
        )


    def validate_name(self, value):
        if len(value) < 257:
            return value
        raise serializers.ValidationError(
            "Name should be 256 length"
        )


class TitlesPostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')
    class Meta:
        fields = '__all__'
        model = Title
    

    def validate_year(self, value):
        if dt.date.today().year < value:
            raise serializers.ValidationError(
                'Wrong year'
            )


class TitlesGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()
    class Meta():
        fields = '__all__'
        read_only_fields = ('id',)
        model = Title


class UsersSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
=======
    class Meta:
        model = User
        fields = (
            'username', 'bio', 'email',
            'first_name', 'last_name', 'role'
        )


class UsersMeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    role = serializers.StringRelatedField(read_only=True)

>>>>>>> 3d3632af8e5ab3a30b84e2e5d3362a66bd807341
    class Meta:
        model = User
        fields = (
            'username', 'bio', 'email',
            'first_name', 'last_name', 'role'
        )
        read_only_fields = ('role',)

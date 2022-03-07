import re
import datetime as dt
from django.shortcuts import get_object_or_404
from dkim import ValidationError
from rest_framework import serializers
from api_yamdb.api_yamdb.reviews.models import Title

from reviews.models import Genre, Category


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


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    category = CategorySerializer()

    class Meta:    
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')
    
    def create(self, validated_data):
        genre = validated_data.pop('genre')
        category = validated_data.pop('category')
        if genre is not None:
            genre, status = get_object_or_404(Genre, genre)
        Category, status = get_object_or_404(Category, category)
        title = Title.objects.create(
            **validated_data,
            category=category,
            genre=genre)
        
        return title

    def validate_year(self, value):
        if dt.date.today().year < value:
            raise serializers.ValidationError(
                'Wrong year'
            )

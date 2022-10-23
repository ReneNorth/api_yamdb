from rest_framework import serializers
from titles.models import Category, Genre, Title
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=128,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug',)
        model = Category
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=128,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )
    category = serializers.CharField()

    def create(self, validated_data):
        raw_genres = validated_data.pop('genre')
        category = validated_data.pop('category')

        title = Title.objects.create(
            **validated_data,
            category=get_object_or_404(Category, slug=category),
        )
        for genre in raw_genres:
            title.genre.add(genre)

        return title

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category',
            # 'rating',
        )
        model = Title

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from titles.models import Category, Comment, Genre, Review, Title


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
    genre = GenreSerializer(many=True, read_only=True,)
    category = CategorySerializer(read_only=True)

    def create(self, validated_data):
        title = Title.objects.create(
            **validated_data,
            category=get_object_or_404(
                Category, slug=self.initial_data['category']
            )
        )

        try:
            genre_slugs = self.initial_data.getlist('genre')
        except Exception:
            genre_slugs = self.initial_data.get('genre')

        for slug in genre_slugs:
            title.genre.add(get_object_or_404(Genre, slug=slug))

        return title

    def update(self, instance, validated_data):
        if self.initial_data.get('category'):
            instance.category = get_object_or_404(
                Category, slug=self.initial_data.get('category')
            )
        return super().update(instance, validated_data)

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category',
            # 'rating',
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

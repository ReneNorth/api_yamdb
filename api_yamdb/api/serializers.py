from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title


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
    rating = serializers.SerializerMethodField()

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
            'id', 'name', 'rating', 'year', 'description', 'genre', 'category'
        )
        model = Title

    def get_rating(self, obj):
        """Рассчитывает средний рейтинг произведения и
        вовзращает значение в поле rating сериализатора."""
        # hits DB for each object = needs refactoring
        query_res = Review.objects.filter(title_id=obj.id)
        if query_res.exists():
            return int(query_res.aggregate(Avg('score'))['score__avg'])
        return None


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.PrimaryKeyRelatedField(read_only=True)
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')

    def validate_title(value):
        if value < 1 or value > 10:
            raise ValidationError('Оценка может быть только от 1 до 10')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        extra_kwargs = {
            'author': {'required': True},
            'text': {'required': True},
        }

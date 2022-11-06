from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from rest_framework.exceptions import NotFound
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


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class TitleRetrieveSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True,)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        read_only_fields = ['author', 'title', 'id']
        extra_kwargs = {
            'score': {'required': True},
            'text': {'required': True},
        }

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise ValidationError('Оценка может быть только от 1 до 10')
        return value

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context[
                'request'].parser_context['kwargs']['title_id']
            if Review.objects.filter(author=self.context['request'].user,
                                     title__id=title_id).exists():
                raise ValidationError('Одно ревью на пользователя')
        return data


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

    def validate(self, data):
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        review_id = self.context[
            'request'].parser_context['kwargs']['review_id']
        if Review.objects.filter(id=review_id, title_id=title_id).exists():
            return data
        raise NotFound('Такого title или ревью не существует')

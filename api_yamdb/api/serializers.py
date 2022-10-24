from rest_framework.serializers import ModelSerializer, SlugField, SlugRelatedField
from titles.models import Category, Genre, Title, Review, Comment
from rest_framework.validators import UniqueValidator


class TitleSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title


class CategorySerializer(ModelSerializer):
    slug = SlugField(
        max_length=128,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug',)
        model = Category
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class GenreSerializer(ModelSerializer):
    slug = SlugField(
        max_length=128,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        extra_kwargs = {'url': {'lookup_field': 'slug'}}



class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        
        

from rest_framework.serializers import ModelSerializer, SlugField
from titles.models import Category, Genre, Title
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
        lookup_field = 'slug'


class GenreSerializer(ModelSerializer):
    slug = SlugField(
        max_length=128,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        lookup_field = 'slug'

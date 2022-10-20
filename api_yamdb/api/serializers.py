from rest_framework.serializers import ModelSerializer
from titles.models import Title, Category, Genre


class TitleSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title


class CategorySerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre

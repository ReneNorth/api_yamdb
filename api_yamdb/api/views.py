from rest_framework import viewsets
from titles.models import Title, Category, Genre

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from users.permissions import IsModeratorPermission, OwnerOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (OwnerOrReadOnly, IsModeratorPermission)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (OwnerOrReadOnly, IsModeratorPermission)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (OwnerOrReadOnly, IsModeratorPermission)

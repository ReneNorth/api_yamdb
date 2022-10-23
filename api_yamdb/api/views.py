from rest_framework import viewsets
from titles.models import Category, Genre, Title
from users.permissions import TitleRoutePermission

from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from django.shortcuts import get_object_or_404


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (TitleRoutePermission,)
    pagination_class = LimitOffsetPagination


class CategoryViewSet(
    viewsets.GenericViewSet,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (TitleRoutePermission,)
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(
    viewsets.GenericViewSet,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (TitleRoutePermission,)
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

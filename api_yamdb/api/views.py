from rest_framework import viewsets
from titles.models import Category, Genre, Title, Review, Comment
from users.permissions import TitleRoutePermission

from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReviewSerializer,
                          CommentSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (TitleRoutePermission,)
    pagination_class = LimitOffsetPagination
    # filter_backends = (SearchFilter, DjangoFilterBackend)
    # filter_fields = ('year', 'name',)
    # search_fields = ('name',)
    # filterset_class = TitleFilter

    def get_queryset(self):
        queryset = Title.objects.all().order_by('id')
        category = self.request.query_params.get('category')
        genre = self.request.query_params.get('genre')
        name = self.request.query_params.get('name')
        year = self.request.query_params.get('year')
        if category is not None:
            queryset = (
                queryset.select_related('category')
                .filter(category__slug=category)
            )
        if genre is not None:
            queryset = (
                queryset.select_related('category')
                .filter(genre__slug=genre)
            )
        if name is not None:
            queryset = (
                queryset.filter(name__contains=name)
            )
        if year is not None:
            queryset = (
                queryset.filter(year=year)
            )

        return queryset


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
<<<<<<< HEAD
    search_fields = ('name', 'slug')
=======
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = (TitleRoutePermission,)
>>>>>>> CommentReview

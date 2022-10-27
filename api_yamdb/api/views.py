from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from titles.models import Category, Comment, Genre, Review, Title
from users.permissions import TitleRoutePermission
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (TitleRoutePermission,)
    pagination_class = LimitOffsetPagination

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
    viewsets.GenericViewSet, mixins.DestroyModelMixin,
    mixins.ListModelMixin, mixins.CreateModelMixin
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
    search_fields = ('name', 'slug')


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    
    def create(self, request, title_id):
        # title_id = self.kwargs['title_id']
        
        # перенести эту проверку в сериализатор
        if Review.objects.filter(author_id=self.request.user.pk, title_id=title_id).count() == 0:
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author_id=self.request.user.id, title_id=title_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
                
                
        




class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = (TitleRoutePermission,)

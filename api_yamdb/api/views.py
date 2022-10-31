from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.permissions import (ReviewsAndCommentsRoutePermission,
                               TitleRoutePermission)

from .filters import TitleFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleRetriveSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (TitleRoutePermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('GET', 'RETRIEVE', 'LIST',):
            return TitleRetriveSerializer
        return TitleCreateSerializer

    def get_queryset(self):
        return Title.objects.all().annotate(
            rating=Avg('reviews__score')).order_by('id')


class AbstractView(
    viewsets.GenericViewSet,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    pass


class CategoryViewSet(AbstractView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (TitleRoutePermission,)
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(AbstractView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (TitleRoutePermission,)
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'slug')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewsAndCommentsRoutePermission, ]

    def get_queryset(self):
        return Review.objects.filter(
            title_id=self.kwargs['title_id']).order_by('id')

    def create(self, request, title_id: int) -> Response:
        get_object_or_404(Title, id=title_id)
        if Review.objects.filter(author_id=self.request.user.pk,
                                 title_id=title_id).count() == 0:
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author_id=self.request.user.id,
                                title_id=title_id)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [ReviewsAndCommentsRoutePermission, ]

    def get_queryset(self):
        return Comment.objects.filter(
            title_id=self.kwargs['title_id'],
            review_id=self.kwargs['review_id']).order_by('id')

    def create(self, request, title_id: int, review_id: int) -> Response:
        """Функция создания коммента сначала поверяет, что ревью к
        произведению, существует, затем валидирует данные и при сохранении
        добавляет id автора, тайла и ревью."""
        get_object_or_404(Review, id=review_id, title_id=title_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_id=self.request.user.id,
                            title_id=title_id,
                            review_id=review_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

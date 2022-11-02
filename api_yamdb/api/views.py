from django.db.models import Avg
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.permissions import (ReviewsAndCommentsRoutePermission,
                               TitleRoutePermission)

from .filters import TitleFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleRetrieveSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (TitleRoutePermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list',):
            return TitleRetrieveSerializer
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
            title_id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id,
                        title_id=self.request.parser_context[
                            'kwargs']['title_id'])


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [ReviewsAndCommentsRoutePermission, ]

    def get_queryset(self):
        return Comment.objects.filter(
            title_id=self.kwargs['title_id'],
            review_id=self.kwargs['review_id'])

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id,
                        title_id=self.request.parser_context[
                            'kwargs']['title_id'],
                        review_id=self.request.parser_context[
                            'kwargs']['review_id'])

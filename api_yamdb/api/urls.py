from django.urls import include, path
from rest_framework import routers
from users.views import UserViewSet

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router1 = routers.SimpleRouter()
router1.register(
    r'titles',
    TitleViewSet,
    basename='titles',
)
router1.register(
    r'categories',
    CategoryViewSet,
    basename='categories',
)
router1.register(
    r'genres',
    GenreViewSet,
    basename='genres',
)

router1.register(
    r'users',
    UserViewSet,
    basename='users',
)

router1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet)
router1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet)

urlpatterns = [
    path('v1/', include(router1.urls)),
    path('v1/auth/', include('custom_auth.urls')),
]

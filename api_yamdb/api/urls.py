from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet, MeViewSet
from .views import TitleViewSet, CategoryViewSet, GenreViewSet


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
    'users/me',
    MeViewSet,
    basename='me'
)
router1.register(
    r'users',
    UserViewSet,
    basename='users',

)

urlpatterns = [
    path('v1/', include(router1.urls)),
    path('v1/auth/', include('custom_auth.urls')),
]
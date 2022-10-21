from django.urls import include, path
from rest_framework import routers
from users.views import MeViewSet, UserViewSet

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

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

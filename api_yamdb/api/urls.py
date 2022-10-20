from django.urls import path, include
from rest_framework import routers

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

urlpatterns = [
    path('v1/', include(router1.urls))
]

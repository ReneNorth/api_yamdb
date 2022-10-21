from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters

from .models import User
from .serializers import UserSerializer
from .permissions import IsSuperUser


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser|IsSuperUser, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)


class MeViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return User.objects.get(username=self.kwargs.get('username'))

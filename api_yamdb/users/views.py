from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import User
from .permissions import IsSuperUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | IsSuperUser, ]
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

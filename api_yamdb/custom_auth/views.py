from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from .serializers import ObtainTokenSerializer, SignupSerializer


class ObtainUserTokenView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = ObtainTokenSerializer

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.data.get('confirmation_code')
            user = get_object_or_404(User,
                                     username=request.data.get('username'))
            if confirmation_code == user.confirmation_code:
                return Response(get_token_for_user(user),
                                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = SignupSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_200_OK,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_token_for_user(user):
    access = AccessToken.for_user(user)
    return {
        'token': str(access),
    }

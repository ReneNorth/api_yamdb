from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import generics

from django.shortcuts import get_object_or_404

from .serializers import SignupSerializer
from users.models import User


# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = (AllowAny,)
#
#     serializer_class = MyTokenObtainPairSerializer


class ObtainUserTokenView(APIView):

    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        confirmation_code = request.data['confirmation_code']
        if confirmation_code == user.confirmation_code:
            return Response(get_token_for_user(user))


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer


def get_token_for_user(user):
    access = AccessToken.for_user(user)
    return {
        'token': str(access),
    }

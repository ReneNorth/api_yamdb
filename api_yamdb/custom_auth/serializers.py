import string
import random

from django.core.mail import send_mail

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from users.models import User


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#
#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)
#
#         # Add custom claims
#         token['username'] = user.username
#         return token


class SignupSerializer(serializers.ModelSerializer):
    code_len = 30

    username = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        # TODO: добавить сценарий, когда такой пользователь уже зареган админом
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            confirmation_code=get_confirmation_code(self.code_len)
        )
        user.save()

        send_mail(
            'Код подтверждения для регистрации на сервисе Yamdb',
            f'{user.username}, ваш код подтверждения: {user.confirmation_code}',
            'yamdb_help@example.com',
            [f'{user.email}'],
            fail_silently=False,
        )

        return user

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("You not allowed to use this name. Choose another one!")
        return value


def get_confirmation_code(length):
    """Возвращает строку из случайных символов длиной length."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

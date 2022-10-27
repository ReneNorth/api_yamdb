import random
import string

from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User
from django.shortcuts import get_object_or_404

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#
#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)
#
#         # Add custom claims
#         token['username'] = user.username
#         return token

# class ValidationError400(ValidationError)


class SignupSerializer(serializers.ModelSerializer):
    code_len = 30
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    # email = serializers.EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )

    class Meta:
        model = User
        fields = ('username', 'email')
        extra_kwargs = {
                'is_admin': {'write_only': True}
        }

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
        if value == 'me' or len(User.objects.filter(username=value)) != 0:
            raise serializers.ValidationError("You not allowed to use this name. Choose another one!")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError("You not allowed to use this email. Choose another one!")
        return value


def get_confirmation_code(length):
    """Возвращает строку из случайных символов длиной length."""
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=length)
    )


class ObtainTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def to_internal_value(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        if not username:
            raise serializers.ValidationError({
                'username': 'This field is required.'
            })

        if confirmation_code != get_object_or_404(
                User, username=username).confirmation_code:
            raise serializers.ValidationError({
                'conf code': 'wrong cong code.'
            })

        return data

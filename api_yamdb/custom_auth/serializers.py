import random
import string

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.models import User

CODE_LEN = 30


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')
        extra_kwargs = {
            'is_admin': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            confirmation_code=get_confirmation_code(CODE_LEN)
        )
        user.save()

        send_mail(
            'Код подтверждения для регистрации на сервисе Yamdb',
            f'{user.username}, ваш код подтверждения: ',
            f'{user.confirmation_code} yamdb_help@example.com',
            [f'{user.email}'],
            fail_silently=False,
        )

        return user

    def validate_username(self, value):
        if value == 'me' or User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Это имя занято.'
                                              'Пожалуйста, выберите другое')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Эта почта занята.'
                                              'Пожалуйста, выберите другую')
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

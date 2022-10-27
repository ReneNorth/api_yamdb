from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role', )
        extra_kwargs = {'role': {'read_only': True},
                        'email': {'read_only': True}, }
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def validate_role(self, value):
        if (value == ('admin' or 'moderator')
           and (get_object_or_404(User, pk=self.instance.pk).role == 'user')):
            return 'user'
        return value

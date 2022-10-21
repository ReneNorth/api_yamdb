from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    # REQUIRED_FIELDS = ['username', 'email']

    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(choices=CHOICES, default='user', max_length=128)
    confirmation_code = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(fields=['username', 'email'],
                                    name='unique_user')
        ]

    def __str__(self):
        return self.username

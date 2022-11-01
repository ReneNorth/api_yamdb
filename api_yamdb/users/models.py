from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser:
    USER: str = 'user'
    MODERATOR: str = 'moderator'
    ADMIN: str = 'admin'

    CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(choices=CustomUser.CHOICES,
                            default='user',
                            max_length=128)
    confirmation_code = models.CharField(max_length=30)

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(fields=['username', 'email'],
                                    name='unique_user')
        ]

    @property
    def is_user(self):
        return self.role == CustomUser.USER

    @property
    def is_moderator(self):
        return self.role == CustomUser.MODERATOR

    @property
    def is_admin(self):
        return self.role == CustomUser.ADMIN

    def __str__(self):
        return self.username

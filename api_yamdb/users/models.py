from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
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

    # @property
    # def is_admin(self):
    #     return (
    #         self.role == User.ADMIN
    #         or self.is_superuser
    #     )
        
    # @property
    # def is_moderator(self): 
    #     return self.role == User.MODERATOR
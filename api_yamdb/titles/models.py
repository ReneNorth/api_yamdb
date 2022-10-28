from django.db import models
# from users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=64,
        null=False,
    )
    year = models.IntegerField(
        null=False,
    )
    description = models.TextField(
        null=True,
    )
    category = models.ForeignKey(
        'Category',
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        'Genre',
        related_name='titles',
    )

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=64,
        null=False,
    )
    slug = models.SlugField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['slug', 'name'],
                name='unique category'
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название',
        max_length=64,
        null=False,
    )
    slug = models.SlugField(
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['slug', 'name'],
                name='unique genre'
            ),
        ]

    def __str__(self) -> str:
        return self.name




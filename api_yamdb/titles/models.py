from django.contrib.auth import get_user_model
from django.db import models

from .validators import year_validator

User = get_user_model()


class Title(models.Model):
    year = models.PositiveSmallIntegerField(
        null=False,
        validators=(year_validator,)
    )
    name = models.CharField(
        'Название',
        max_length=64,
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

    class Meta:
        ordering = ['id']

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
        ordering = ['id']
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
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['slug', 'name'],
                name='unique genre'
            ),
        ]

    def __str__(self) -> str:
        return self.name

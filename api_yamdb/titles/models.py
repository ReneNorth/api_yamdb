from django.db import models


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=64,
        null=False,
    )
    year = models.IntegerField(
    )
    rating = models.IntegerField(
    )
    description = models.TextField(
    )
    category = models.ForeignKey(
        'Category',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=64,
        null=False,
    )
    slug = models.SlugField(
    )

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
    # Not sure about it, but should work
    title = models.ManyToManyField(
        'Title',
        related_name='genres',
    )

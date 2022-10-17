from django.db import models


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=64,
        null=False,
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

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название',
        max_length=64,
        null=False,
    )
    # Not sure about it, but should work
    title = models.ManyToManyField(
        'Title',
        related_name='genres',
    )

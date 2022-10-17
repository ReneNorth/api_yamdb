from django.db import models


class Title(models.Model):

    title = models.CharField(
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

    # Temp fields for plug, ForiegnKey in future
    geners = models.IntegerField()

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

from django.db import models

class Title(models.Model):

    title = models.CharField(
        'Название',
        max_length=64,
        null=False,
    )

    # Temp fields for plug, ForiegnKey in future
    category = models.IntegerField()
    geners = models.IntegerField()

    def __str__(self) -> str:
        return self.title
from django.db import models


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
<<<<<<< HEAD

    def __str__(self):
        return self.name
=======
        
    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    text = models.TextField()
    score = models.PositiveSmallIntegerField(default=0)
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        null=True)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    def __str__(self) -> str:
        return f'comment id: {self.id}, text: {self.text[:15]}'
    # добавить ограничение оцнека от 1 до 10
    # дату автодобавление 
    # название отображается неверно в админке


class Comment(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True)
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True
    )
    pub_date = models.DateTimeField(
        auto_now_add=True)

    def __str__(self) -> str:
        return f'comment id: {self.id}, text: {self.text[:15]}'
>>>>>>> CommentReview

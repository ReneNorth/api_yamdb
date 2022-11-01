from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from titles.models import Title

User = get_user_model()


class Review(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author')
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        default=5,
        validators=[MaxValueValidator(10, 'Оценка должна быть от 1 до 10'),
                    MinValueValidator(1, 'Оценка должна быть от 1 до 10')]
    )
    title = models.ForeignKey(Title,
                              related_name='reviews',
                              on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'
        unique_together = ('author', 'title',)
        ordering = ['id']

    def __str__(self) -> str:
        return (f'review id: {self.id}, '
                f'text: {self.text[:15]}, '
                f'rating: {self.score}')


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    title = models.ForeignKey(Title,
                              related_name='comments',
                              on_delete=models.CASCADE)
    review = models.ForeignKey(Review,
                               related_name='comments',
                               on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return f'comment id: {self.id}, text: {self.text[:15]}'

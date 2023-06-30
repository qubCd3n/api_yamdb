from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import max_length_validator
from users.models import User
from api_yamdb.settings import VALUE_MAX_VAL, VALUE_MIN_VAL


class Review(models.Model):
    """Отзыв к произведениям."""
    text = models.TextField('Отзыв')
    author = models.ForeignKey(
        User,
        related_name='review_author',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    # title = models.ForeignKey(
    # Title,
    # on_delete=models.CASCADE,
    #  related_name='reviews',
    #  verbose_name='Произведение',
   # )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=(
            MinValueValidator(VALUE_MIN_VAL), MaxValueValidator(VALUE_MAX_VAL)
        ),
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзыв'

    def __str__(self):
        return f'{self.text} - {self.score}'


class Comment(models.Model):
    """Комментарии к произведениям."""
    text = models.TextField('Коментарий', validators=(max_length_validator,))
    author = models.ForeignKey(
        User,
        related_name='comment_author',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text

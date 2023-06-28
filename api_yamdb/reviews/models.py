from django.db import models

from .validators import max_length_validator


class Reviews(models.Model):
    """Отзывы."""
    pass


class Comment(models.Model):
    """Коментарий."""
    pass

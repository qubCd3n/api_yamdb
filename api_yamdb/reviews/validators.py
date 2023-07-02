from django.core.exceptions import ValidationError

MAX_VALUE_COMMENT = 3000


def max_length_validator(value):
    """Проверка макс длины комментария."""
    if len(value) > MAX_VALUE_COMMENT:
        raise ValidationError(
            f'Длина комментария {value}'
            f'не может быть больше {MAX_VALUE_COMMENT}',
            params={"value": value},
        )

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from rest_framework.serializers import ModelSerializer, ValidationError
from users.models import User
from reviews.models import Comment, Review
from api_yamdb.settings import VALUE_MAX_VAL, VALUE_MIN_VAL

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(r'^[\w.@+-]+$', max_length=150)
    email = serializers.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя!')
        return username

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if (User.objects.filter(username=username).exists()
           and not User.objects.filter(email=email).exists()):
            raise serializers.ValidationError('Такой username уже есть!')

        if (User.objects.filter(email=email).exists()
           and not User.objects.filter(username=username).exists()):
            raise serializers.ValidationError(
                'Ваш email уже зарегистрирован!'
            )
        return super().validate(data)


class TokenReceiveSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True,
    )


class ReviewSerializer(serializers.ModelSerializer):
    """Серилизатор Review."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )
    score = serializers.IntegerField(
        required=True,
        validators=(
            MaxValueValidator(VALUE_MAX_VAL),
            MinValueValidator(VALUE_MIN_VAL))
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title', 'author')


class CommentSerializer(serializers.ModelSerializer):
    """Серилизатор Comment."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Comment
        read_only_fields = ('author', 'review')
        exclude = ('review',)

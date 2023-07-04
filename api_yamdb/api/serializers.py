from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (ModelSerializer, SlugRelatedField,
                                        ValidationError)
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = 'name', 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = 'name', 'slug'


class TitleWriteSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='slug', many=True,
                             queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, year):
        present_year = timezone.now().year
        if year > present_year:
            raise serializers.ValidationError(
                'Год выпуска фильма не может быть больше текущего года!')
        if year < 1895:
            raise serializers.ValidationError('Кино еще не появилось!')
        return year


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise ValidationError(
                'Это ошибка, вызванная тем, что нельзя оставлять'
                'два отзыва на одно произведение'
            )
        return data


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


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
    username = serializers.RegexField(
        r'^[\w.@+-]+$',
        max_length=150,
    )
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя \'me\' в качестве username запрещено!'
            )
        return username

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user_obj_email = (User.objects.filter(email=email).exists())
        user_obj_username = User.objects.filter(username=username).exists()
        if user_obj_username and not user_obj_email:
            raise serializers.ValidationError(
                'Использовать \'username\' зарегистрированного'
                ' пользователя и незанятый \'email\' запрещено'
            )
        if user_obj_email and not user_obj_username:
            raise serializers.ValidationError(
                'Использовать \'email\' зарегистрированного пользователя'
                ' и незанятый \'username\' запрещено'
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

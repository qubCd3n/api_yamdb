from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from reviews.models import Cathegory, Genre, Title

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


class CategorySerializer(serializers.ModelSerializer):
    """Серилиазатор Category."""

    class Meta:
        model = Cathegory
        exlude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    """Серилиазатор Genre."""

    class Meta:
        model = Genre
        exlude = ['id']


class TitleSerializer(serializers.ModelSerializer):
    """Серилиазатор Title."""

    categoty = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

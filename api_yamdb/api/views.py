from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAdminOrModeratorOrOwnerOrReadOnly)

from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          TokenReceiveSerializer, UserRegistrationSerializer,
                          UserSerializer, ReviewSerializer, CommentSerializer,)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title

from api_yamdb.settings import EMAIL

from .permissions import (IsAdmin, IsAdminOrModeratorOrOwnerOrReadOnly,
                          IsAdminOrReadOnly, IsAuthenticated,
                          IsAuthenticatedOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TokenReceiveSerializer, UserRegistrationSerializer,
                          UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    http_method_names = ('get', 'post', 'patch', 'detele')

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            data = request.data.dict()
            if 'role' in data:
                data.pop('role')
            serializer = UserSerializer(request.user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenReceiveViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = TokenReceiveSerializer

    def create(self, request):
        serializer = TokenReceiveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            data = {'token': str(AccessToken.for_user(user))}
            return Response(data, status=status.HTTP_200_OK)
        return Response(
            "wrong confirmation code",
            status=status.HTTP_400_BAD_REQUEST
        )


class UserRegistrationViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):

        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        print(confirmation_code)
        send_mail(
            subject='Код подтверждения.',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=EMAIL,
            recipient_list=(user.email,),
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет для ReviewSerializer."""
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAdminOrModeratorOrOwnerOrReadOnly, IsAuthenticatedOrReadOnly,
    )

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для CommentSerializer."""
    serializer_class = CommentSerializer
    permission_classes = (
        IsAdminOrModeratorOrOwnerOrReadOnly, IsAuthenticatedOrReadOnly,
    )

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    
class UserRegistrationViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    "Вьюсет для регистрации."
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        print(confirmation_code)
        send_mail(
            subject='Код подтверждения.',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=EMAIL,
            recipient_list=(user.email,),
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

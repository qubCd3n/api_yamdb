from rest_framework import viewsets, status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsAdmin
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    TokenReceiveSerializer,
    ReviewSerializer,
    CommentSerializer,
)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    lookup_field = 'username'
    filter_backends = ('username', )
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


class UserRegistrationViewSet():
    serializer_class = UserRegistrationSerializer
    pass


class TokenReceiveViewSet():
    serializer_class = TokenReceiveSerializer
    pass


class ReviewsViewSet():
    serializer_class = ReviewSerializer
    pass


class CommentViewSet():
    serializer_class = CommentSerializer
    pass

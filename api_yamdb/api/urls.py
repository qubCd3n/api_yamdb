from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, TokenReceiveViewSet,
                    UserRegistrationViewSet, UserViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'auth/token/',
        TokenReceiveViewSet.as_view({'post': 'create'}, name='token'),
    ),
    path(
        'auth/signup/',
        UserRegistrationViewSet.as_view({'post': 'create'}, name='user'),
    ),
]

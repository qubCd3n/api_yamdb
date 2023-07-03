from django.urls import include, path
from rest_framework.routers import DefaultRouter

<<<<<<< HEAD
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewsViewSet, TitleViewSet, TokenReceiveViewSet,
                    UserRegistrationViewSet, UserViewSet)
=======
from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    TokenReceiveViewSet, ReviewsViewSet, CommentViewSet,
                    UserRegistrationViewSet)
>>>>>>> c2fca82 (Исправил пару ошибок)

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
        CommentViewSet,
        basename='comment'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenReceiveViewSet.as_view({'post': 'create'}),),
    path('auth/signup/', UserRegistrationViewSet.as_view({'post': 'create'}),),
]

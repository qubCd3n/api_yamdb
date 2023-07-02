from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, ReviewsViewSet, CommentViewSet
                    TokenReceiveViewSet, UserRegistrationViewSet, UserViewSet)

router = DefaultRouter()


router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename= 'genres')
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
    path('auth/signup/',UserRegistrationViewSet.as_view({'post': 'create'}),),
  
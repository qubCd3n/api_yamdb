from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, ReviewsViewSet, CommentViewSet
                    TokenReceiveViewSet, UserRegistrationViewSet, UserViewSet)

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename= 'genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('auth/token/', TokenReceiveViewSet.as_view({'post': 'create'}),),
    # path('auth/signup/',UserRegistrationViewSet.as_view({'post': 'create'}),),
]

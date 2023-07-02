from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    TokenReceiveViewSet, UserRegistrationViewSet, UserViewSet)

router = DefaultRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename= 'genres')
router.register('titles', TitleViewSet, basename='titles')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenReceiveViewSet.as_view({'post': 'create'}),),
    path('auth/signup/',UserRegistrationViewSet.as_view({'post': 'create'}),),

]

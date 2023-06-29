from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TokenReceiveViewSet, UserRegistrationViewSet


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/token/', TokenReceiveViewSet.as_view({'post': 'create'}),),
    # path('auth/signup/',UserRegistrationViewSet.as_view({'post': 'create'}),),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'platforms', PlatformViewSet)
router.register(r'pages', PageViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'images', ImageViewSet)
router.register(r'comments', PlaceCommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]



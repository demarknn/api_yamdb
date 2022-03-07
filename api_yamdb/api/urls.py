from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet


router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('genres', TitleViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
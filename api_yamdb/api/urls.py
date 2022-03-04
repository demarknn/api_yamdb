from rest_framework.routers import SimpleRouter
from django.urls import include, path
from .views import (
    ReviewsViewSet, CommentsViewSet, RegistrationAPIView,
    LoginView, UsersViewSet
)


v1_router = SimpleRouter()
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
v1_router.register(
    'users',
    UsersViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', LoginView.as_view(), name='login'),
]

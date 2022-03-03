from rest_framework.routers import SimpleRouter
from django.urls import include, path
from reviews.views import RegistrationAPIView, LoginView
from .views import ReviewsViewSet, CommentsViewSet


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

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/singup/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', LoginView.as_view(), name='token_obtain_pair'),
]

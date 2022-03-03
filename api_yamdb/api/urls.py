from rest_framework.routers import DefaultRouter
from django.urls import include, path
from reviews.views import RegistrationAPIView, LoginView


urlpatterns = [
    path('v1/singup/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', LoginView.as_view(), name='token_obtain_pair'),

]




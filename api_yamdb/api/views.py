from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from reviews.models import Reviews, Title, User
from api.serializers import (
    CommentSerializer,
    ReviewsSerializer,
    RegistrationSerializer,
    UsersSerializer,
    LoginSerializer
)
from api.permissions import (
    UserPermission,
    AdminPermission,
    ModeratorPermission,
    MeUserPermission
)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [
        AdminPermission, ModeratorPermission, MeUserPermission
    ]

    def get_title(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title

    def get_queryset(self):
        title = self.get_title()
        return title.reviews

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        AdminPermission, ModeratorPermission, MeUserPermission
    ]

    def get_review(self):
        review = get_object_or_404(Reviews, pk=self.kwargs.get("review_id"))
        return review

    def get_queryset(self):
        review = self.get_review()
        return review.comments

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.data['confirmation_code']
        if user.confirmation_code != confirmation_code:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        },
            status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AdminPermission, ]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=['GET', 'PATCH'], url_path='me',
            permission_classes=(UserPermission,))
    def me(self, request):
        userself = User.objects.get(username=self.request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(userself)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = self.get_serializer(userself, data=request.data,
                                             partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

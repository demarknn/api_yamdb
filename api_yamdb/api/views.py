from rest_framework import viewsets, mixins, filters
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

from reviews.models import Review, Title, User, Genre, Category
from api.serializers import (
    CommentSerializer,
    ReviewsSerializer,
    RegistrationSerializer,
    UsersSerializer,
    LoginSerializer,
    GenreSerializer,
    CategorySerializer,
    TitlesGetSerializer,
    UsersMeSerializer,
    TitlesPostSerializer
)
from api.permissions import (
    UserPermission,
    AdminPermission,
    AdminOrReadOnly,
    AdminModeratorAuthorPermission,
)
from .filters import TitleFilter


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [
        AdminModeratorAuthorPermission
    ]

    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title

    def get_queryset(self):
        title = self.get_title()
        queryset = title.reviews.order_by('id')
        return queryset

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        AdminModeratorAuthorPermission
    ]

    def get_review(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

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
        serializer = UsersMeSerializer(request.user)
        userself = User.objects.get(username=self.request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(userself)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UsersMeSerializer(
                userself, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UsersMeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersMeSerializer
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


class DeleteCreateListRetrieveGenericViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(DeleteCreateListRetrieveGenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='genre_slug'
    )
    def get_genre(self, request, slug):
        genre = self.get_object()
        serializer = GenreSerializer(genre)
        genre.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(DeleteCreateListRetrieveGenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_category(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesGetSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitlesPostSerializer
        return TitlesGetSerializer

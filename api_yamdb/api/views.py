from rest_framework import viewsets, mixins, filters
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes

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


def send_code(user):
    send_mail(
        user.username,
        user.confirmation_code,
        'from@yamdb.ru',
        [user.email],
    )


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


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    user.confirmation_code = default_token_generator.make_token(user)
    send_code(user)
    user.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def code_recovery(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    user = get_object_or_404(User, username=username, email=email)
    user.confirmation_code = default_token_generator.make_token(user)
    user.save()
    send_code(user)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer_class = LoginSerializer
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data['confirmation_code']
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


class DeleteCreateListRetrieveGenericViewSet(
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet
):
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
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('-id')
    serializer_class = TitlesGetSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitlesPostSerializer
        return TitlesGetSerializer

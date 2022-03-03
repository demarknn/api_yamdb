from rest_framework import viewsets

from django.shortcuts import get_object_or_404

from reviews.models import Reviews, Title
from api.serializers import (
    CommentsSerializer,
    ReviewsSerializer
)
from api.permissions import IsAuthorOrModeratorOrAdminOrReadOnly


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthorOrModeratorOrAdminOrReadOnly, ]

    def get_title(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title

    def get_reviews(self):
        title = self.get_title()
        return title.reviews

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorOrModeratorOrAdminOrReadOnly, ]

    def get_review(self):
        review = get_object_or_404(Reviews, pk=self.kwargs.get("review_id"))
        return review

    def get_queryset(self):
        review = self.get_review()
        return review.comments

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)

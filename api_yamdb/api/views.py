from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Categories, Comment, Genres, Review, Titles
from users.models import User

# from .permissions import (CanEditAdminContent, CanEditUserContentPermission,
#                           CanReadPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer, UserSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.annotate(avg_rating=Avg('reviews__score'))
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (CanEditUserContentPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        new_queryset = title_id.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title_id = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title_id)

    def perform_update(self, serializer):
        pass


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (CanEditUserContentPermission,)
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review_id.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, title=review_id)


class UserViewSet(viewsets.ModelViewSet):
    pass

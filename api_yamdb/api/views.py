from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, filters
from rest_framework.settings import api_settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from reviews.models import Categories, Comment, Genres, Review, Titles
from users.models import User

from .permissions import (CanEditAdminContent, CanEditUserContentPermission,
                          CanReadPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer)


class ListCreateDeleteViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (CanEditAdminContent,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_fields = 'slug'
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (CanEditAdminContent,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_fields = 'slug'
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (CanEditAdminContent,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug',
                        'genre__slug',
                        'name',
                        'year')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (CanEditUserContentPermission,)
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
    permission_classes = (CanEditUserContentPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review_id.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, title=review_id)


class UserViewSet(viewsets.ModelViewSet):
    pass

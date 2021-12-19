import random
import string


from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, viewsets, filters, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.settings import api_settings

from reviews.models import Category, Comment, Genre, Review, Title
from users.utils import generate_auth_code
from api_yamdb.settings import AUTH_CODE_LENGTH, AUTH_FROM_EMAIL

from .permissions import (AdminOnlyPermission, AdminOrReadOnlyPermission,
                          AdminOrModeratorOrAuthorPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer, AuthCodeSerializer, SendAuthCodeSerializer,
                          ProfileSerializer)

User = get_user_model()


class ListCreateDeleteViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_fields = 'slug'
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_fields = 'slug'
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug',
                        'genre__slug',
                        'name',
                        'year')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminOrModeratorOrAuthorPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title_id.reviews.all()

    def perform_create(self, serializer):
        title_id = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title_id)

    def perform_update(self, serializer):
        pass


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminOrModeratorOrAuthorPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review_id.comments.all()

    def perform_create(self, serializer):
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review_id)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AdminOnlyPermission]
    lookup_field = 'username'


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_auth_code(request):
    serializer = SendAuthCodeSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data['username']
        email = request.data['email']
        user_exists = (User.objects.filter(username=username).exists()
                       or User.objects.filter(email=email).exists())
        if not user_exists:
            User.objects.create_user(email=email, username=username)
        auth_code = generate_auth_code(AUTH_CODE_LENGTH)
        user = User.objects.get(username=username)
        User.objects.filter(username=username).update(
            auth_code=auth_code
        )
        email_subject = 'Ваш код подтверждения'
        email_message = f'Используйте код подтверждения {auth_code}, чтобы авторизоваться'
        send_mail(subject=email_subject, message=email_message,
                  recipient_list=[user.email], from_email=AUTH_FROM_EMAIL)
        return Response(
            {
                'message': f'Сообщение успешно отправлено пользователю {username}'
            },
            status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = AuthCodeSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data['username']
        user = get_object_or_404(User, username=username)
        if user.auth_code == request.data['confirmation_code']:
            access_token = AccessToken.for_user(user)
            return Response(
                {
                    'error': None,
                    'token': f'{access_token}'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'error': 'Неверный код подтверждения',
                'token': None
            }
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
@permission_classes([permissions.AllowAny])
def profile(request):
    if not request.user.is_authenticated:
        return Response('Not authorized', status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    serializer = ProfileSerializer(request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



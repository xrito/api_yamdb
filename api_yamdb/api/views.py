import random
import string

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model


from reviews.models import Categories, Comment, Genres, Review, Titles
from users.utils import generate_auth_code
from api_yamdb.settings import AUTH_CODE_LENGTH, AUTH_FROM_EMAIL

from .permissions import (AdminOnlyPermission, AdminOrReadOnlyPermission,
                          AdminOrModeratorOrAuthorPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer, AuthCodeSerializer, SendAuthCodeSerializer)

User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminOrModeratorOrAuthorPermission,)
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
    permission_classes = (AdminOrModeratorOrAuthorPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review_id.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, title=review_id)


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
        send_mail(subject=email_subject, message=email_message, recipient_list=[user.email], from_email=AUTH_FROM_EMAIL)
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
        if(user.auth_code == request.data['confirmation_code']):
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

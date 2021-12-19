from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
import datetime as dt

from reviews.models import (Categories, Genres, GenreTitles, Titles, Review,
                            Comment)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role']
        lookup_field = 'username'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(slug_field='slug',
                             many=True,
                             required=True
                             )
    category = SlugRelatedField(slug_field='slug',
                                required=True
                                )
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Titles
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=GenreTitles.objects.all(),
                fields=('title', 'genre')
            ),
            UniqueTogetherValidator(
                queryset=Titles.objects.all(),
                fields=('name', 'category')
            )
        ]

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value

    def validate_genre(self, values):
        for value in values:
            if not Genres.objects.filter(slug=value):
                raise serializers.ValidationError(
                    'Такого жанра не существует!')
            return value

    def validate_category(self, value):
        if not Categories.objects.filter(slug=value):
            raise serializers.ValidationError(
                'Такой категории не существует!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    titles = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class AuthCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class SendAuthCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    username = serializers.CharField(
        required=True,
    )

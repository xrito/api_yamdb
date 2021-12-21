import datetime as dt

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+\Z", required=True, max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']
        lookup_field = 'username'


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+\Z", required=False, max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=False, max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name',
                  'last_name', 'bio', 'role']
        read_only_fields = ['role']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleListSerializer(serializers.ModelSerializer):

    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'description', 'year', 'rating']


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(slug_field='slug',
                             required=True,
                             many=True,
                             queryset=Genre.objects.all())
    category = SlugRelatedField(slug_field='slug',
                                required=True,
                                queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'description', 'year']

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value

    def validate_genre(self, values):
        for value in values:
            if not Genre.objects.filter(slug=value):
                raise serializers.ValidationError(
                    'Такого жанра не существует!')
            return value

    def validate_category(self, value):
        if not Category.objects.filter(slug=value):
            raise serializers.ValidationError(
                'Такой категории не существует!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        author = self.context['request'].user
        title = (self.context['request'].parser_context['kwargs']['title_id'])
        if Review.objects.filter(author=author, title_id=title).exists():
            raise serializers.ValidationError()
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date']
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

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Вы не можете использовать этот username')
        return value

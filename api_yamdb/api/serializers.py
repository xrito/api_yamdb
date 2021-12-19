from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Categories, Genres, Titles, Review, Comment
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    pass


class ReviewSerializer(serializers.ModelSerializer):
    titles = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class TitleSerializer(serializers.ModelSerializer):
    avg_rating = serializers.IntegerField(read_only=True, required=False)


    class Meta:
        model = Titles
        fields = '__all__'

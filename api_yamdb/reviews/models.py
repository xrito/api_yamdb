from django.db import models
from django.conf import settings


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True,)
    genre = models.ManyToManyField(
        Genres,
        through='GenreTitles',
        through_fields=('title', 'genre'))
    category = models.ForeignKey(
        Categories,
        related_name='categories',
        on_delete=models.SET_NULL,
        null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class GenreTitles(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.SET_NULL,
        null=True)
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
        null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre'
            )
        ]


class Review(models.Model):
    DEFAULT_CHOICES = (
        (10, '10'),
        (9, '9'),
        (8, '8'),
        (7, '7'),
        (6, '6'),
        (5, '5'),
        (4, '4'),
        (3, '3'),
        (2, '2'),
        (1, '1'),
    )
    titles = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        choices=DEFAULT_CHOICES,
        default=0,
        blank=False
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    # class Meta:
    #     # не дает повторно ставить  писать ревью
    #     unique_together = ('author', 'titles')

    def __str__(self):
        return self.author.username


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text

from django.conf import settings
from django.db import models


class Review(models.Model):
    DEFAULT_CHOICES = (
        ('10', '10'),
        ('9', '9'),
        ('8', '8'),
        ('7', '7'),
        ('6', '6'),
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
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

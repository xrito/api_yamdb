from __future__ import print_function

import os
import csv

from django.core.management.base import BaseCommand

from reviews.models import Categories, Genres, Comment, Review, Titles
from users.models import User

from glob import glob


class Command(BaseCommand):
    help = 'Импорт данных из csv в db.'

    def handle(self, *args, **options):
        # csv_file = './static/data/category.csv'

        for csv_file in glob('./static/data/*.csv'):
            # if not os.path.isfile(csv_file):
            #     print('ФАЙЛ НЕ НАЙДЕН')
            #     return
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if os.path.basename(csv_file) == os.path.basename(
                            r'./static/data/category.csv'):
                        category, created = Categories.objects.update_or_create(
                            id=int(row['id']), name=row['name'],
                            slug=row['slug']
                        )
                    if os.path.basename(csv_file) == os.path.basename(
                            r'./static/data/genre.csv'):
                        genre, created = Genres.objects.update_or_create(
                            id=int(row['id']), name=row['name'],
                            slug=row['slug']
                        )
                    if os.path.basename(csv_file) == os.path.basename(
                            r'./static/data/titles.csv'):
                        titles, created = Titles.objects.update_or_create(
                            id=int(row['id']), name=row['name'],
                            year=row['year'], category_id=row['category']
                        )
                    if os.path.basename(csv_file) == os.path.basename(
                            r'./static/data/users.csv'):
                        users, created = User.objects.update_or_create(
                            id=int(row['id']), username=row['username'],
                            email=row['email'], role=row['role']
                        )
        for csv_file in glob('./static/data/*.csv'):
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if os.path.basename(csv_file) == os.path.basename(
                            r'./static/data/review.csv'):
                        review, created = Review.objects.update_or_create(
                            id=int(row['id']), titles_id=row['title_id'],
                            text=row['text'], author_id=row['author'],
                            score=row['score'], pub_date=row['pub_date']
                        )
        for csv_file in glob('./static/data/*.csv'):
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if os.path.basename(csv_file) == os.path.basename(
                            r'./static/data/comments.csv'):
                        comments, created = Comment.objects.update_or_create(
                            id=int(row['id']), review_id=row['review_id'],
                            text=row['text'], author_id=row['author'],
                            pub_date=row['pub_date']
                        )
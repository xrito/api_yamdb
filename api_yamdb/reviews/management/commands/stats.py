from __future__ import print_function

import os
import csv

from django.core.management.base import BaseCommand

from reviews.models import Categories


class Command(BaseCommand):
    help = 'Импорт данных из csv в db.'

    def handle(self, *args, **options):
        csv_file = './static/data/category.csv'

        if not os.path.isfile(csv_file):
            print('ФАЙЛ НЕ НАЙДЕН')
            return

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:

                category, created = Categories.objects.update_or_create(
                    id=int(row['id']), name=row['name'],
                    slug=row['slug'])

import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category, Comments, Genre, Reviews, Title, User

TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Reviews: 'review.csv',
    Comments: 'comments.csv'
}


class Command(BaseCommand):
    help = "Loads products and product categories from CSV file."

    def handle(self, *args, **kwargs):
        for model, csv_d in TABLES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_d}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
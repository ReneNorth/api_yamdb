import csv

from django.shortcuts import get_object_or_404
from users.models import User

from ..models import Category, Genre, Title


def genres():
    with open('api_yamdb/static/data/genre.csv',
              encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:

            Genre.objects.get_or_create(
                name=row[1],
                slug=row[2],
            )


def users():
    with open('api_yamdb/static/data/users.csv',
              encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:

            User.objects.get_or_create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6],
            )


def titles():
    with open('api_yamdb/static/data/titles.csv',
              encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:

            Title.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=get_object_or_404(Category, id=row[3]),
            )


def categories():
    with open('api_yamdb/static/data/category.csv',
              encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:

            Category.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2],
            )


def set_genres():
    with open(
        'api_yamdb/static/data/genre_title.csv', encoding='utf-8'
    ) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            title = get_object_or_404(Title, id=row[1])
            genre = get_object_or_404(Genre, id=row[2])
            title.genre.add(genre)


def run():
    users()
    genres()
    categories()
    titles()
    set_genres()

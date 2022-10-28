from django.contrib import admin
from titles.models import Category, Genre, Title

admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)

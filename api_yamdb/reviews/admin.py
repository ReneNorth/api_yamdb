from django.contrib import admin
from reviews.models import Comment, Review


@admin.register(Review, Comment)
class Admin(admin.ModelAdmin):
    pass

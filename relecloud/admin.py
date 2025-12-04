from django.contrib import admin
from .models import Destination, Review

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "destination", "rating", "title", "created_at")
    list_filter = ("destination", "rating")
    search_fields = ("title", "comment", "user__username")

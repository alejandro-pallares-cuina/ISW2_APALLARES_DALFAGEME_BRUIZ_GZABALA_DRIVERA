from django.contrib import admin
from .models import Destination, Review

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name",)
#Desde admin.py registramos el modelo Destination para que sea accesible desde el panel de administración de Django.
#Desde el admin ya puedes subir imágenes. Se guardan correctamente en /media/destinations/ .Django sirve esas imágenes si MEDIA_URL está bien configurado

# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "destination", "rating", "title", "created_at")
    list_filter = ("destination", "rating")
    search_fields = ("title", "comment", "user__username")

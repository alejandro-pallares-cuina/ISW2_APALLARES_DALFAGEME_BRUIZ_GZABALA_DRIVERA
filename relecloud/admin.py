from django.contrib import admin
from . import models

#Desde admin.py registramos el modelo Destination para que sea accesible desde el panel de administración de Django.
#Desde el admin ya puedes subir imágenes. Se guardan correctamente en /media/destinations/ .Django sirve esas imágenes si MEDIA_URL está bien configurado

# Register your models here.

admin.site.register(models.Destination)

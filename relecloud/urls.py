## APP (relecloud)

from django.urls import path #Te ayuda a identificar como vamos a hacer la ruta
from . import views

urlpatterns = [
    path('', views.index, name='index'), #lleva la petición desde el project y si el request está vacío, redirige a la función de vista "index"
    path('about', views.about , name='about'),
    #path('destinations', views.destinations , name='destinations'),
    path('destinations/', views.destinations, name='destinations'),
    path('destination/<int:pk>', views.DestinationDetailView.as_view(), name='destination_detail'), 
    path('cruise/<int:pk>', views.CruiseDetailView.as_view(), name='cruise_detail'), path( 'info_request', views.InfoRequestCreate.as_view(), name='info_request'),
    path('info_request', views.InfoRequestCreate.as_view(), name='info_request'),
]
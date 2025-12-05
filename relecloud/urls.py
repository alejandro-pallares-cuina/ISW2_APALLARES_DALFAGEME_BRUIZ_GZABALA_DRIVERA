from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('destinations/', views.destinations, name='destinations'),
    path('destination/<int:pk>', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('cruise/<int:pk>', views.CruiseDetailView.as_view(), name='cruise_detail'),
    path('info_request', views.InfoRequestCreate.as_view(), name='info_request'),

    # CREATE review para un destino
    path(
        'destinations/<int:destination_id>/reviews/create/',
        views.create_destination_review,
        name='destination_review_create'
    ),

    # UPDATE review
    path(
        'reviews/<int:review_id>/edit/',
        views.update_review,
        name='review_update'
    ),

    # DELETE review
    path(
        'reviews/<int:review_id>/delete/',
        views.delete_review,
        name='review_delete'
    ),
]

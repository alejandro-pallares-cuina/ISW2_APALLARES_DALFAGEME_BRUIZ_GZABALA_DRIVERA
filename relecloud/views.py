from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Avg

from .forms import ReviewForm


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def destinations(request):
    all_destinations = models.Destination.objects.all()
    return render(request, 'destinations.html', {'destinations': all_destinations})


class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        """
        T6: añadir al contexto:
        - reviews del destino
        - valoración media
        - formulario de review (si el usuario puede crearla)
        """
        context = super().get_context_data(**kwargs)
        destination = self.object

        reviews = destination.reviews.all()
        context["reviews"] = reviews

        avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"]
        context["avg_rating"] = avg_rating

        user = self.request.user
        can_review = user.is_authenticated and user_has_purchase(user)
        context["can_review"] = can_review

        if can_review:
            context["review_form"] = ReviewForm()

        return context


class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'


class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'


def user_has_purchase(user):
    """
    T4: Implementar restricción de compra.

    Versión simplificada:
    - El usuario con username 'buyer' se considera comprador.
    - El resto NO tienen compra.
    """
    return user.username == "buyer"


@login_required
def create_destination_review(request, destination_id):
    """
    CREATE: crea una review para un Destination concreto.

    T4 + T6:
    - Solo usuario con compra puede crear review.
    - El formulario se muestra en el detalle del destino.
    """
    destination = get_object_or_404(models.Destination, pk=destination_id)

    if request.method == "POST":
        if not user_has_purchase(request.user):
            return HttpResponseForbidden(
                "You are not allowed to create a review for this destination."
            )

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.destination = destination
            review.save()

        return redirect('destination_detail', pk=destination_id)

    return redirect('destination_detail', pk=destination_id)


@login_required
def update_review(request, review_id):
    """
    UPDATE: permite al autor de la review editar su propia review.
    """
    review = get_object_or_404(models.Review, pk=review_id)

    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this review.")

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()

        if review.destination:
            return redirect('destination_detail', pk=review.destination.id)
        elif review.cruise:
            return redirect('cruise_detail', pk=review.cruise.id)
        return redirect('index')

    form = ReviewForm(instance=review)
    context = {
        "review": review,
        "form": form,
    }
    return render(request, "review_edit.html", context)


@login_required
def delete_review(request, review_id):
    """
    DELETE: permite al autor borrar su propia review.
    """
    review = get_object_or_404(models.Review, pk=review_id)

    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    if request.method == "POST":
        destination = review.destination
        cruise = review.cruise
        review.delete()

        if destination:
            return redirect('destination_detail', pk=destination.id)
        elif cruise:
            return redirect('cruise_detail', pk=cruise.id)
        return redirect('index')

    context = {
        "review": review,
    }
    return render(request, "review_confirm_delete.html", context)

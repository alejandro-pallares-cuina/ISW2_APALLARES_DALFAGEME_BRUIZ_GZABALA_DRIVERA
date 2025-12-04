from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def user_has_purchase(user):
    """
    T4: Implementar restricción de compra.

    ⚠️ Versión simplificada para esta práctica:
    - Consideramos que el usuario con username 'buyer' es comprador.
    - El resto NO tienen compra.

    En una versión más avanzada, aquí se comprobaría una tabla de compras,
    reservas, etc.
    """
    return user.username == "buyer"


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


@login_required
def create_destination_review(request, destination_id):
    """
    CREATE: crea una review para un Destination concreto.

    T4: Restricción para Reviews:
    - Usuario registrado y con compra -> puede crear review
    - Resto -> creación denegada (403)
    """
    destination = get_object_or_404(models.Destination, pk=destination_id)

    if request.method == "POST":
        # 🔒 Restricción de compra (T4)
        if not user_has_purchase(request.user):
            # Usuario autenticado PERO sin compra -> 403 Forbidden
            return HttpResponseForbidden("You are not allowed to create a review for this destination.")

        rating = request.POST.get("rating")
        title = request.POST.get("title", "")
        comment = request.POST.get("comment", "")

        if rating:
            models.Review.objects.create(
                user=request.user,
                destination=destination,
                rating=rating,
                title=title,
                comment=comment,
            )

        # Redirigimos al detalle del destino (302)
        return redirect('destination_detail', pk=destination_id)

    # Si no es POST, redirigimos también al detalle
    return redirect('destination_detail', pk=destination_id)

@login_required
def update_review(request, review_id):
    """
    UPDATE: permite al autor de la review editar su propia review.
    """
    review = get_object_or_404(models.Review, pk=review_id)

    # Solo el autor puede editar
    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this review.")

    if request.method == "POST":
        rating = request.POST.get("rating")
        title = request.POST.get("title", "")
        comment = request.POST.get("comment", "")

        if rating:
            review.rating = rating
            review.title = title
            review.comment = comment
            review.save()

        # Volvemos al detalle del destino asociado
        if review.destination:
            return redirect('destination_detail', pk=review.destination.id)
        elif review.cruise:
            return redirect('cruise_detail', pk=review.cruise.id)

        return redirect('index')

    # GET: mostrar formulario con datos actuales
    context = {
        "review": review,
    }
    return render(request, "review_edit.html", context)


@login_required
def delete_review(request, review_id):
    """
    DELETE: permite al autor borrar su propia review.
    """
    review = get_object_or_404(models.Review, pk=review_id)

    # Solo el autor puede borrar
    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    if request.method == "POST":
        # Guardamos destino/crucero antes de borrar
        destination = review.destination
        cruise = review.cruise
        review.delete()

        if destination:
            return redirect('destination_detail', pk=destination.id)
        elif cruise:
            return redirect('cruise_detail', pk=cruise.id)

        return redirect('index')

    # GET: mostrar pantalla de confirmación
    context = {
        "review": review,
    }
    return render(request, "review_confirm_delete.html", context)

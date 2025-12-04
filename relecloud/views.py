from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from .email_service import send_info_request_email

# Create your views here.
# Http response se encarga de evolver una petición
# request tiene toda la infromación del usuario, como las cookies o el form. 

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def destinations(request):
    all_destinations = models.Destination.objects.all()
    return render(request, 'destinations.html', {'destinations': all_destinations})

class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models. Destination
    context_object_name = 'destination'

class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models. Cruise
    context_object_name = 'cruise'

class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'

    def get_form(self, form_class=None):
        """Customize form labels and help text."""
        form = super().get_form(form_class)
        form.fields['name'].label = 'Full Name'
        form.fields['name'].help_text = 'Your full name'
        form.fields['email'].label = 'Email Address'
        form.fields['email'].help_text = 'We will send a confirmation to this email'
        form.fields['cruise'].label = 'Cruise'
        form.fields['cruise'].help_text = 'Select the cruise you are interested in'
        form.fields['notes'].label = 'Additional Notes'
        form.fields['notes'].help_text = 'Any additional information or questions (optional)'
        form.fields['notes'].required = False
        return form

    def form_valid(self, form):
        """Handle form submission: save and send confirmation email."""
        response = super().form_valid(form)
        # Send confirmation email to the requester
        send_info_request_email(
            to_email=form.cleaned_data['email'],
            name=form.cleaned_data['name'],
            cruise=str(form.cleaned_data['cruise'])
        )
        return response
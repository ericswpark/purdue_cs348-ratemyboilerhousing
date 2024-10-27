from django.views.generic import ListView, DetailView

from core.models import Housing, Offering


class HomeView(ListView):
    template_name = "home.html"
    model = Housing
    context_object_name = "housing_options"

class HousingView(DetailView):
    template_name = "housing.html"
    model = Housing

class OfferingView(DetailView):
    template_name = "offering.html"
    model = Offering
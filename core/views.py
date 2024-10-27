from django.views.generic import ListView

from core.models import Housing


class HomeView(ListView):
    template_name = "home.html"
    model = Housing
    context_object_name = "housing_options"
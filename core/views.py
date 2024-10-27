from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.models import Housing, Offering, Review


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

class CreateReviewView(LoginRequiredMixin, CreateView):
    template_name = "create_review.html"
    model = Review
    fields = ['stars', 'description']

    def form_valid(self, form):
        offering_id = self.kwargs['pk']

        offering = Offering.objects.get(pk=offering_id)
        form.instance.offering = offering

        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        offering_id = self.kwargs['pk']
        return reverse('offering_detail', kwargs={'pk': offering_id})

class EditReviewView(LoginRequiredMixin, UpdateView):
    template_name = "edit_review.html"
    model = Review
    fields = ['stars', 'description']

    def get_success_url(self):
        offering = self.object.offering
        return reverse('offering_detail', kwargs={'pk': offering.id})

class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "delete_review.html"

    def get_success_url(self):
        offering = self.object.offering
        return reverse('offering_detail', kwargs={'pk': offering.id})

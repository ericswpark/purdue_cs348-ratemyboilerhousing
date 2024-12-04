from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from core.models import Housing, Offering, Review, Statistics


class HomeView(ListView):
    template_name = "home.html"
    model = Housing
    context_object_name = "housing_options"

class ReviewFilterView(ListView):
    template_name = "reviews_filter.html"
    model = Review

    default_stars = 1

    def get_queryset(self):
        stars = self.request.GET.get('stars', self.default_stars)
        price_min = self.request.GET.get('price_min', Offering.get_min_cost())
        price_max = self.request.GET.get('price_max', Offering.get_max_cost())
        return Review.objects.filter(
            stars__gte=(int(stars) * 2), # Dirty hack
            offering__cost__gte=price_min,
            offering__cost__lte=price_max
        )

    def get_context_data(self, **kwargs):
        context = super(ReviewFilterView, self).get_context_data(**kwargs)
        context['stars'] = self.request.GET.get('stars', self.default_stars)
        context['price_min'] = self.request.GET.get('price_min', Offering.get_min_cost())
        context['price_max'] = self.request.GET.get('price_max', Offering.get_max_cost())
        context['price_abs_min'] = Offering.get_min_cost()
        context['price_abs_max'] = Offering.get_max_cost()
        return context



class HousingView(DetailView):
    template_name = "housing.html"
    model = Housing

class OfferingView(DetailView):
    template_name = "offering.html"
    model = Offering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user:
            return False
        user_has_review = Review.objects.filter(user=self.request.user, offering=self.object).exists()
        context['user_has_review'] = user_has_review
        return context

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


@method_decorator(staff_member_required, name='dispatch')
class AdminStatsView(TemplateView):
    template_name = "admin_stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stat_object'] = Statistics.get_today_stats()
        return context
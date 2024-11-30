from django.urls import path

from core.views import HomeView, HousingView, OfferingView, CreateReviewView, EditReviewView, DeleteReviewView, \
    ReviewFilterView, AdminStatsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('housing/<int:pk>/', HousingView.as_view(), name='housing_detail'),
    path('offering/<int:pk>/', OfferingView.as_view(), name='offering_detail'),
    path('offering/<int:pk>/write_review/', CreateReviewView.as_view(), name='offering_write_review'),
    path('review/<int:pk>/edit/', EditReviewView.as_view(), name='edit_review'),
    path('review/<int:pk>/delete/', DeleteReviewView.as_view(), name='delete_review'),
    path("reviews/filter/", ReviewFilterView.as_view(), name='reviews_filter'),
    path("stats/", AdminStatsView.as_view(), name="admin_stats"),
]

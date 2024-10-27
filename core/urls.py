from django.urls import path

from core.views import HomeView, HousingView, OfferingView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('housing/<int:pk>/', HousingView.as_view(), name='housing_detail'),
    path('offering/<int:pk>/', OfferingView.as_view(), name='offering_detail'),
]

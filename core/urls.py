from django.urls import path

from core.views import HomeView, HousingView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('housing/<int:pk>/', HousingView.as_view(), name='housing_detail')
]

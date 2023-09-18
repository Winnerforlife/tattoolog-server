from django.urls import path
from .views import CountryFilterView, CityFilterView

urlpatterns = [
    path('cities/', CityFilterView.as_view(), name='city-list'),
    path('countries/', CountryFilterView.as_view(), name='country-list'),
]

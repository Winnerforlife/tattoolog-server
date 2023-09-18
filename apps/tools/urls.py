from django.urls import path
from .views import CountryFilterView

urlpatterns = [
    path('countries/', CountryFilterView.as_view(), name='country-list'),
]

from django.urls import path
from apps.tools.views import CountryFilterView, CityFilterView, PartnersView, BlogDetailView, BlogListView, \
    RatingCreateView, FestivalListView, FestivalDetailView

urlpatterns = [
    path('cities/', CityFilterView.as_view(), name='city-list'),
    path('countries/', CountryFilterView.as_view(), name='country-list'),
    path('partners/', PartnersView.as_view(), name='partners'),
    path('blogs/', BlogListView.as_view(), name='blogs-list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('rating/', RatingCreateView.as_view(), name='rating'),
    path('festival/', FestivalListView.as_view(), name='festivals-list'),
    path('festival/<int:pk>/', FestivalDetailView.as_view(), name='festival-detail'),
]

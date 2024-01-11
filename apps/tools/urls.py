from django.urls import path
from apps.tools.views import (CountryFilterView, CityFilterView, PartnersView, RatingCreateView, AssociationTypeApiView,
                              FestivalListView, FestivalDetailView, BlogPostListView, BlogPostDetailView)

urlpatterns = [
    path('cities/', CityFilterView.as_view(), name='city-list'),
    path('countries/', CountryFilterView.as_view(), name='country-list'),
    path('partners/', PartnersView.as_view(), name='partners'),
    path('rating/', RatingCreateView.as_view(), name='rating'),
    path('association-type/', AssociationTypeApiView.as_view(), name='association-type'),
    path('festival/', FestivalListView.as_view(), name='festivals-list'),
    path('festival/<str:slug>/', FestivalDetailView.as_view(), name='festival-detail'),
    path('blogs/', BlogPostListView.as_view(), name='blog-list'),
    path('blog/<str:slug>/<str:language>/', BlogPostDetailView.as_view(), name='blog-detail'),
]

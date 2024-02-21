from django.urls import path
from apps.tools.views import (CountryFilterView, CityFilterView, PartnersView, RatingCreateView, AssociationTypeApiView,
                              FestivalListView, FestivalDetailView, BlogPostListView, BlogPostDetailView,
                              BlogCategoryListView, FestivalCategoryListView, ProjectApiView,
                              FestivalPhotoVoteCreateView, FestivalPhotoSubmissionCreateView)

urlpatterns = [
    path('cities/', CityFilterView.as_view(), name='city-list'),
    path('countries/', CountryFilterView.as_view(), name='country-list'),
    path('partners/', PartnersView.as_view(), name='partners'),
    path('rating/', RatingCreateView.as_view(), name='rating'),
    path('association-type/', AssociationTypeApiView.as_view(), name='association-type'),
    path('projects-type/', ProjectApiView.as_view(), name='projects-type'),
    path('festivals/', FestivalListView.as_view(), name='festivals-list'),
    path('festival/<str:slug>/', FestivalDetailView.as_view(), name='festival-detail'),
    path('festivals/category/', FestivalCategoryListView.as_view(), name='festival-category-list'),
    path('festival/photo/create/', FestivalPhotoSubmissionCreateView.as_view(), name='festival-photo'),
    path('festival/photo/vote/', FestivalPhotoVoteCreateView.as_view(), name='festival-photo-vote'),
    path('blogs/', BlogPostListView.as_view(), name='blog-list'),
    path('blog/<str:slug>/<str:language>/', BlogPostDetailView.as_view(), name='blog-detail'),
    path('blogs/category/', BlogCategoryListView.as_view(), name='blog-category-list'),
]

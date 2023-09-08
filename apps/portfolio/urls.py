from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.portfolio.views import PostViewSet, ProfilePostsApiView

router = SimpleRouter()

router.register("post", PostViewSet, basename="post")

urlpatterns = [
    path('posts/profile/<int:user_id>/', ProfilePostsApiView.as_view(), name='user-posts-list'),
] + router.urls

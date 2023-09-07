from rest_framework.routers import SimpleRouter

from apps.portfolio.views import PostViewSet

router = SimpleRouter()

router.register("post", PostViewSet, basename="post")

urlpatterns = [
] + router.urls

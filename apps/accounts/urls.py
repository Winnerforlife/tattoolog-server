from rest_framework.routers import SimpleRouter

from apps.accounts.views import ProfileViewSet

router = SimpleRouter()

router.register("profiles", ProfileViewSet, basename="profiles")

urlpatterns = [
] + router.urls

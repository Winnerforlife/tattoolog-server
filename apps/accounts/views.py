import requests

from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apps.accounts.models import Profile
from apps.accounts.serializers import ProfileSerializer

domain = Site.objects.get_current().domain


def activation_view(request, uid, token):
    activation_url = f"{settings.SITE_PROTOCOL}://{domain}/api/v1/users/activation/"
    data = {"uid": uid, "token": token}
    response = requests.post(activation_url, data=data)

    if response.status_code == 204:
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/error/')


@extend_schema(
    description=(
        'Field "user" represents the profile ID because the Profile model uses CustomUser model'
        ' as the primary key for a one-to-one relationship.'
    )
)
class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]

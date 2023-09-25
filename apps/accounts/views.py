import requests

from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apps.accounts.filters import ProfileFilter
from apps.accounts.models import Profile
from apps.accounts.serializers import ProfileSerializer, ProfileFilterSerializer, CRMIntegrationProfiles

domain = Site.objects.get_current().domain


def activation_view(request, uid, token):
    activation_url = f"{settings.SITE_PROTOCOL}://{domain}/auth/users/activation/"
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


@extend_schema(
    summary='Retrieving all profiles of a specific role.',
    description=(
        'Using optional parameters: **name**, **city**, **country**. You can filter the final result.\n'
        '* name - filters by the fields first_name and last_name.\n'
        '* city - filters by the field city.\n'
        '* country - filters by the field country.'
    )
)
class ProfileApiView(ListAPIView):
    serializer_class = ProfileFilterSerializer
    permission_classes = [AllowAny]
    filterset_class = ProfileFilter

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Profile.objects.none()
        role = self.kwargs['role']
        return Profile.objects.filter(user__role=role)


@extend_schema(
    summary='Retrieving all profiles for CRM integration.',
    description=(
        'Using optional parameter: **date**. You can filter the final result.\n'
        '* date - filters by the date create account from input date to today.'
    )
)
class CRMIntegrationProfilesAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = CRMIntegrationProfiles
    permission_classes = [AllowAny]

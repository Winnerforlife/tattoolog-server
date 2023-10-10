import requests
from datetime import datetime

from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.accounts.filters import ProfileFilter
from apps.accounts.models import Profile
from apps.accounts.serializers import ProfileSerializer, ProfileFilterSerializer, CRMIntegrationProfiles
from apps.tools.utils import CustomPagination

domain = Site.objects.get_current().domain


def activation_view(request, uid, token):
    activation_url = f"{settings.SITE_PROTOCOL}://{domain}/auth/users/activation/"
    data = {"uid": uid, "token": token}
    response = requests.post(activation_url, data=data)

    if response.status_code == 204:
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/error/')


def reset_password_redirect(request, uid, token):
    redirect_url = f"/set_new_password?uid={uid}&token={token}"
    return redirect(redirect_url)


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

    # ToDo убрать ненужные ендпоинты
    # http_method_names = ['get', 'patch']

    def retrieve_profile(self, request, *args, **kwargs):
        instance = self.get_object()
        current_user = request.user
        if request.method == 'GET' and instance.user != current_user:
            instance.count_visit += 1
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve_profile(request, *args, **kwargs)
        return super().retrieve(request, *args, **kwargs)


@extend_schema(
    summary='Retrieving all profiles of a specific role. (Default pagination size 10 objects)',
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
    pagination_class = CustomPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Profile.objects.none()
        role = self.kwargs['role']
        return Profile.objects.filter(user__role=role)


@extend_schema(
    summary='Retrieving all profiles for CRM integration.',
    description=(
        'Using optional parameter: **date**. You can filter the final result.\n'
        '* date - Filters the result by account creation date relative to the entered date.'
    )
)
class CRMIntegrationProfilesAPIView(ListAPIView):
    serializer_class = CRMIntegrationProfiles
    permission_classes = [AllowAny]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Profile.objects.none()
        date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d')
        return Profile.objects.filter(user__date_joined__gte=date)

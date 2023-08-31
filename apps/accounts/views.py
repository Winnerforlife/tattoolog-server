import requests

from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.conf import settings

domain = Site.objects.get_current().domain


def activation_view(request, uid, token):
    activation_url = f"{settings.SITE_PROTOCOL}://{domain}/api/v1/users/activation/"
    data = {"uid": uid, "token": token}
    response = requests.post(activation_url, data=data)

    if response.status_code == 204:
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/error/')

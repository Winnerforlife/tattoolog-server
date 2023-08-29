from django.http import HttpResponseRedirect
import requests
from django.urls import reverse


def activation_view(request, uid, token):
    activation_url = f"http://0.0.0.0:8000/api/v1/users/activation/"

    return requests.post(activation_url, data={"uid": uid, "token": token}) and HttpResponseRedirect('/')


# import urllib.parse
# import urllib.request
#
# def activation_view(request, uid, token):
#     # Формируем данные для POST-запроса
#     data = {
#         'uid': uid,
#         'token': token
#     }
#     data_encoded = urllib.parse.urlencode(data).encode('utf-8')
#
#     # Выполняем POST-запрос к эндпоинту активации пользователя
#     activation_url = reverse('user-activation')  # Замените на правильное имя представления
#     response = urllib.request.urlopen(activation_url, data=data_encoded)
#
#     # Проверяем успешность запроса и редирект
#     if response.getcode() == 200:
#         return HttpResponseRedirect('/')
#     else:
#         return HttpResponse('Ошибка активации пользователя')
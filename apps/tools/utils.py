import requests
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


def send_sms(phone_number, message):
    url = "https://sms-fly.ua/api/v2/api.php"
    api_key = '8CFXQHR8OT1CMHXLGQMFO5EVEUY541EO'

    if not phone_number or not message:
        return Response({'error': 'Требуются номер телефона и сообщение'}, status=status.HTTP_400_BAD_REQUEST)

    data = {
        "auth": {
            "key": api_key
        },
        "action": "SENDMESSAGE",
        "data": {
            "recipient": phone_number,
            "channels": ["sms"],
            "sms": {
                "source": "Tattoo Log",
                "ttl": 300,
                "flash": 0,
                "text": message
            }
        }
    }
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return Response({'message': 'СМС отправлено успешно'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Ошибка при отправке СМС'}, status=status.HTTP_400_BAD_REQUEST)

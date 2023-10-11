import json
import requests
from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.sites.models import Site
from django.utils import timezone
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.accounts.models import CustomUser, Profile

from cities_light.models import Country, City

from apps.tools.models import SocialMediaType, Rating


class ProfileViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data_1 = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'salon',
        }
        self.user_data_2 = {
            'email': 'test2@example.com',
            'first_name': 'Piter',
            'last_name': 'Parker',
            'role': 'salon',
        }

        self.user1 = CustomUser.objects.create_user(**self.user_data_1)
        self.user2 = CustomUser.objects.create_user(**self.user_data_2)

        file_content = b"Test file content"
        avatar = SimpleUploadedFile("test_file.png", file_content, content_type="image/png")
        self.country = Country.objects.create(name='United States')
        self.city = City.objects.create(name='New York', country=self.country)

        self.profile = Profile.objects.get(user=self.user1)
        self.profile.avatar = avatar
        self.profile.salons_and_masters.add(self.user2),
        self.profile.about = 'Test about me'
        self.profile.address = '1-st street 12/45'
        self.profile.birthday = timezone.datetime(1990, 1, 1).date()
        self.profile.phone_number = '+48123456789'
        self.profile.country = self.country
        self.profile.city = self.city
        self.profile.save()

        self.social_media_type = SocialMediaType.objects.create(name='Facebook')

        self.profile_2 = Profile.objects.get(user=self.user2)

    def test_patch_profile(self):
        """
        {
          "user": {
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "role": "master"
          },
          "avatar": "string",
          "salons_and_masters": [
            0
          ],
          "about": "string",
          "status": "pending",
          "country": 0,
          "city": 0,
          "address": "string",
          "birthday": "2023-10-02",
          "phone_number": "string",
          "social_media_profile": [
            {
              "social_media_type": {
                "name": "string"
              },
              "link": "string"
            }
          ],
          "count_visit": 32767
        }
        """
        data_to_update = {
            "user": {
                "first_name": "New First Name",
                "last_name": "New Last Name",
                "role": "master"
            },
            # "avatar": self.profile.avatar,
            "salons_and_masters": [
                self.user2.id
            ],
            "about": "New about me",
            "status": "approved",
            "country": self.country.id,
            "city": self.city.id,
            "address": "New address",
            "birthday": "2023-10-02",
            "phone_number": "+48731731731",
            "social_media_profile": [
                {
                    "social_media_type": {
                        "name": self.social_media_type.name
                    },
                    "link": "http://example.com"
                }
            ],
        }
        url = reverse('profile-detail', args=[self.profile.user_id])
        response = self.client.patch(url, data=json.dumps(data_to_update), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.user.first_name, data_to_update["user"]["first_name"])
        self.assertEqual(self.profile.user.last_name, data_to_update["user"]["last_name"])
        self.assertEqual(self.profile.user.role, data_to_update["user"]["role"])
        # self.assertEqual(self.profile.avatar, data_to_update["avatar"])
        self.assertEqual(self.profile.about, data_to_update["about"])
        self.assertEqual(self.profile.address, data_to_update["address"])
        self.assertEqual(str(self.profile.birthday), data_to_update["birthday"])
        self.assertEqual(self.profile.phone_number, data_to_update["phone_number"])
        self.assertEqual(self.profile.count_visit, 0)
        self.client.get(url)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.count_visit, 1)

    # ToDo реализовать функцию для некорректных данных
    def test_patch_profile_invalid_data(self):
        pass

    def test_ditail_profile(self):
        url = reverse('profile-detail', args=[self.profile.user_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['user']['email'], self.user_data_1['email'])
        self.assertEqual(response.data['user']['first_name'], self.user_data_1['first_name'])
        self.assertEqual(response.data['user']['last_name'], self.user_data_1['last_name'])
        self.assertEqual(response.data['user']['role'], self.user_data_1['role'])
        self.assertEqual(response.data['avatar'], f"http://testserver{self.profile.avatar.url}")
        self.assertEqual(response.data['about'], self.profile.about)
        self.assertEqual(response.data['address'], self.profile.address)
        self.assertEqual(response.data['birthday'], str(self.profile.birthday))
        self.assertEqual(response.data['phone_number'], self.profile.phone_number)
        self.assertEqual(response.data['country'], self.profile.country.id)
        self.assertEqual(response.data['city'], self.profile.city.id)

    def test_get_average_rating(self):
        url_1 = reverse('profile-detail', args=[self.profile.user_id])

        Rating.objects.create(profile=self.profile, mark=4, comment='Good')
        Rating.objects.create(profile=self.profile, mark=5, comment='Norm')

        response = self.client.get(url_1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_rating'], 4.5)

        url_2 = reverse('profile-detail', args=[self.profile_2.user_id])
        response = self.client.get(url_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['average_rating'], 0)

    def test_list_profile(self):
        url = reverse('profile-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileApiViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data_1 = {
            'email': 'test1@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'salon',
        }

        self.user1 = CustomUser.objects.create_user(**self.user_data_1)

        self.profile = Profile.objects.get(user=self.user1)

    def test_profile_list(self):
        url = reverse('role-profile-list', kwargs={'role': 'salon'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        url = reverse('role-profile-list', kwargs={'role': 'master'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)


    # ToDo Дописать тесты для получения данный в CRM
# class CRMIntegrationProfilesAPIViewTest(APITestCase):
#     """
#     [
#       {
#         "user": {
#           "id": 0,
#           "email": "user@example.com",
#           "first_name": "string",
#           "last_name": "string",
#           "role": "master"
#         },
#         "post_profile": [
#           {
#             "id": 0,
#             "profile": 0,
#             "work_type": {
#               "id": 0,
#               "name": "string",
#               "description": "string"
#             },
#             "photo_post": [
#               {
#                 "id": 0,
#                 "post": 0,
#                 "photo": "string"
#               }
#             ],
#             "description": "string",
#             "created_at": "2023-10-02T13:39:44.204Z"
#           }
#         ],
#         "about": "string",
#         "social_media_profile": [
#           {
#             "social_media_type": {
#               "name": "string"
#             },
#             "link": "string"
#           }
#         ],
#         "phone_number": "string"
#       }
#     ]
#     """
#     def setUp(self):
#         self.client = APIClient()
#
#         self.user_data_1 = {
#             'email': 'test@example.com',
#             'first_name': 'John',
#             'last_name': 'Doe',
#             'role': 'salon',
#         }
#         self.user_data_2 = {
#             'email': 'test2@example.com',
#             'first_name': 'Piter',
#             'last_name': 'Parker',
#             'role': 'salon',
#         }
#
#         self.user1 = CustomUser.objects.create_user(**self.user_data_1)
#         self.user2 = CustomUser.objects.create_user(**self.user_data_2)
#
#         file_content = b"Test file content"
#         avatar = SimpleUploadedFile("test_file.png", file_content, content_type="image/png")
#         self.country = Country.objects.create(name='United States')
#         self.city = City.objects.create(name='New York', country=self.country)
#
#         self.profile = Profile.objects.get(user=self.user1)
#         self.profile.avatar = avatar
#         self.profile.salons_and_masters.add(self.user2),
#         self.profile.about = 'Test about me'
#         self.profile.address = '1-st street 12/45'
#         self.profile.birthday = timezone.datetime(1990, 1, 1).date()
#         self.profile.phone_number = '+48123456789'
#         self.profile.country = self.country
#         self.profile.city = self.city
#         self.profile.save()
#
#         self.social_media_type = SocialMediaType.objects.create(name='Facebook')
#         self.date = datetime.now().strftime('%Y-%m-%d')
#
#     def test_crm_integration_profiles(self):
#         url = reverse('integration-crm', kwargs={'date': self.date})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

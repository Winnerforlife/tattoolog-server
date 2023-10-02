"""
Для каждого ендпоинта отдельный класс: class {endpoint name}Test():

Для каждого метода отдельная функция:
    [GET] def test_list_{func name}(self):
    [POST] def test_create_{func name}(self):
           def test_create_{func name}_invalid_data(self):

Внутри класса указать ожидаемые данные:
    {
      "photos": [
        "string"
      ],
      "post": 0
    }
"""
import tempfile

from PIL import Image
from io import BytesIO

from datetime import datetime

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.accounts.models import Profile, CustomUser
from apps.portfolio.models import WorkType, Post, Photo


class PhotoCreateViewTest(APITestCase):
    """
    {
      "photos": [
        "string"
      ],
      "post": 0
    }
    """
    def setUp(self):
        self.client = APIClient()

        self.user_data_1 = {
            'email': 'test@example.com',
            'first_name': 'JohnPhoto',
            'last_name': 'Doe',
            'role': 'salon',
        }
        self.user_1 = CustomUser.objects.create_user(**self.user_data_1)
        self.profile_1 = Profile.objects.get(user=self.user_1)

        self.work_type = WorkType.objects.create(name="Classic", description="Description for classic work type")

        self.created_at = timezone.now()
        self.post_data_1 = {
            'profile': self.profile_1,
            'description': 'Description for post',
            'created_at': self.created_at,
            'work_type': self.work_type
        }
        self.post_1 = Post.objects.create(**self.post_data_1)

        self.url = reverse('post-photo')

    def get_test_mediafile_data(self):
        image = Image.new('RGB', (100, 100))
        image_io = BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)

        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_file.write(image_io.read())
        temp_file.seek(0)

        return temp_file

    def test_create_photo(self):
        self.assertEqual(Photo.objects.count(), 0)
        with self.get_test_mediafile_data() as image_file1, \
                self.get_test_mediafile_data() as image_file2:
            photo_data = {
                'post': self.post_1.id,
                'photos': [image_file1, image_file2]
            }
            response = self.client.post(self.url, photo_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Photo.objects.count(), 2)
        self.assertEqual(Photo.objects.filter(post=self.post_1).count(), 2)

    def test_create_photo_invalid_data(self):
        self.assertEqual(Photo.objects.count(), 0)
        with self.get_test_mediafile_data() as image_file1:
            photo_data = {
                'post': self.post_1,
                'photos': image_file1
            }
            response = self.client.post(self.url, photo_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['post'][0].code, 'incorrect_type')
        self.assertEqual(
            str(response.data['post'][0]),
            'Incorrect type. Expected pk value, received str.'
        )


class WorkTypeApiViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.work_type = WorkType.objects.create(name="Classic", description="Description for classic work type")

    def test_list_work_types(self):
        url = reverse('work_types')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data[0]['id'], self.work_type.id)
        self.assertEqual(response_data[0]['name'], self.work_type.name)
        self.assertEqual(response_data[0]['description'], self.work_type.description)


class PostCreateApiViewTest(APITestCase):
    """
    URL: post/create/

    {
      "profile": 0,
      "description": "string",
      "work_type": 0,
      "created_at": "2023-09-29T13:06:10.884Z"
    }
    """
    def setUp(self):
        self.client = APIClient()

        self.user_data_1 = {
            'email': 'test@example.com',
            'first_name': 'JohnPost',
            'last_name': 'Doe',
            'role': 'salon',
        }
        self.user_1 = CustomUser.objects.create_user(**self.user_data_1)
        self.profile_1 = Profile.objects.get(user=self.user_1)

        self.work_type = WorkType.objects.create(name="Classic", description="Description for classic work type")

        self.created_at = timezone.now()

        self.url = reverse('post')

    def test_create_post(self):
        post_data_1 = {
            'profile': self.profile_1.user_id,
            'description': 'Description for post_1',
            'created_at': self.created_at,
            'work_type': self.work_type.id
        }

        response = self.client.post(self.url, post_data_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_invalid_data(self):
        post_data_2 = {
            'profile': self.profile_1.user_id,
            'description': 'Description for post_2',
            'created_at': self.created_at,
            'work_type': self.work_type.name
        }

        response = self.client.post(self.url, post_data_2, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('work_type', response.data)
        self.assertEqual(response.data['work_type'][0].code, 'incorrect_type')
        self.assertEqual(
            str(response.data['work_type'][0]),
            'Incorrect type. Expected pk value, received str.'
        )


class ProfilePostsApiViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data_1 = {
            'email': 'test@example.com',
            'first_name': 'JohnProfile',
            'last_name': 'DoePosts',
            'role': 'salon',
        }
        self.user_1 = CustomUser.objects.create_user(**self.user_data_1)
        self.profile_1 = Profile.objects.get(user=self.user_1)

        self.work_type = WorkType.objects.create(name="Classic", description="Description for classic work type")

        self.created_at = timezone.now()
        self.post_data_1 = {
            'profile': self.profile_1,
            'description': 'Description for post_1',
            'created_at': self.created_at,
            'work_type': self.work_type
        }
        self.post_1 = Post.objects.create(**self.post_data_1)

    def test_list_posts_for_user(self):
        url = reverse('user-posts-list', args=[self.profile_1.user_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data[0]['work_type']['id'], self.work_type.id)
        self.assertEqual(response_data[0]['description'], self.post_1.description)
        self.assertEqual(datetime.fromisoformat(response_data[0]['created_at']), self.post_1.created_at)

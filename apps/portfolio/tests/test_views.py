from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Profile, CustomUser
from apps.portfolio.models import WorkType, Post


class PostViewSetTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'salon',
        }
        self.user_data_2 = {
            'email': 'piter@example.com',
            'first_name': 'Piter',
            'last_name': 'Parker',
            'role': 'master',
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.user_2 = CustomUser.objects.create_user(**self.user_data_2)

        self.file_content = b"Test file content"
        self.avatar = SimpleUploadedFile("test_file.png", self.file_content, content_type="image/png")

        self.profile_data = {
            'user': self.user,
            'avatar': self.avatar,
            'about': 'Test about me',
            'status': 'approved',
        }
        self.profile = Profile.objects.create(**self.profile_data)
        self.profile.salons_and_masters.add(self.user_2)

        self.work_type_data = {
            'name': 'Test name',
            'description': 'Test description'
        }
        self.work_type = WorkType.objects.create(**self.work_type_data)

        self.post_data = {
            'profile': self.profile,
            'description': 'Test Description',
            'work_type': self.work_type,
        }
        self.post = Post.objects.create(**self.post_data)

        self.uploaded_file_1 = SimpleUploadedFile("test_image1.png", self.file_content)
        self.uploaded_file_2 = SimpleUploadedFile("test_image2.jpg", self.file_content)

    def test_create_post(self):
        url = reverse('post-list')
        data = {
                'profile': self.profile.user_id,
                "photo_post": [
                    {"photo": self.uploaded_file_1},
                    {"photo": self.uploaded_file_2}
                ],
                'description': 'Test Description',
                'work_type': self.work_type.id,
                "created_at": "2023-09-07T11:06:55.038Z",
            }

        response = self.client.post(url, data, format='multipart')
        print(f'{response.data} - response.data')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_retrieve_post(self):
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        url = reverse('post-detail', args=[self.post.id])
        updated_data = {
            'description': 'Updated Description',
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.description, 'Updated Description')

    def test_delete_post(self):
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_list_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
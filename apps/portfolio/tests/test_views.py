import base64
import tempfile

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
        self.user = CustomUser.objects.create_user(**self.user_data)

        self.file_content = b"Test file content"
        self.avatar = SimpleUploadedFile("test_file.png", self.file_content, content_type="image/png")

        self.profile_data = {
            'user': self.user,
            'avatar': self.avatar,
            'about': 'Test about me',
            'status': 'approved',
        }
        self.profile = Profile.objects.create(**self.profile_data)

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

        self.uploaded_file = SimpleUploadedFile("test_image.png", self.file_content, content_type="image/png")

    def get_test_mediafile_data(self):
        with tempfile.NamedTemporaryFile(suffix='.png') as temp_file:
            temp_file.write(b"Test file content")
            temp_file.seek(0)

            file_content_base64 = base64.b64encode(temp_file.read()).decode('utf-8')

            return {
                'profile': self.profile.user.id,
                'description': 'Test Description',
                'work_type': self.work_type.id,
                "photo_post": [
                    {"photo": file_content_base64},
                ],
            }

    def test_create_post(self):
        url = reverse('post-list')
        # with tempfile.NamedTemporaryFile(suffix='.png') as temp_file:
        #     temp_file.write(b"Test file content")
        #     temp_file.seek(0)
        #
        # # encoded_image = base64.b64encode(self.uploaded_file.read()).decode('utf-8')
        # file_content_base64 = base64.b64encode(temp_file.read()).decode('utf-8')
        # data = {
        #     'profile': self.profile.user.id,
        #     'description': 'Test Description',
        #     'work_type': self.work_type.id,
        #     "photo_post": [
        #         {"photo": file_content_base64},
        #     ],
        # }
        data = self.get_test_mediafile_data()
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Post.objects.count(), 2)

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
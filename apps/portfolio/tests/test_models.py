from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import CustomUser, Profile
from apps.portfolio.models import WorkType, Post, Photo


class ModelTestCase(TestCase):
    def setUp(self):
        self.user_data_1 = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'salon',
        }

        self.user_1 = CustomUser.objects.create_user(**self.user_data_1)
        self.profile = Profile.objects.get(user=self.user_1)

        self.work_type_data = {
            'name': 'Development',
            'description': 'test work_type description',
        }
        self.work_type = WorkType.objects.create(**self.work_type_data)

        self.post_data = {
            'profile': self.profile,
            'description': 'Test post description',
            'created_at': timezone.now(),
            'work_type': self.work_type
        }
        self.post = Post.objects.create(**self.post_data)

        self.file_content = b"Test file content"
        self.post_photo = SimpleUploadedFile("test_file.png", self.file_content, content_type="image/png")
        self.photo_data = {
            'post': self.post,
            'photo': self.post_photo
        }
        self.photo = Photo.objects.create(**self.photo_data)

    def test_work_type_creation(self):
        self.assertEqual(self.work_type.name, 'Development')
        self.assertEqual(self.work_type.description, 'test work_type description')

    def test_photo_creation(self):
        self.assertEqual(self.photo.post, self.post)
        self.assertEqual(self.photo.photo.file.read(), self.file_content)

    def test_post_creation(self):
        self.assertEqual(self.post.profile, self.profile)
        self.assertEqual(self.post.description, 'Test post description')
        self.assertEqual(self.post.work_type, self.work_type)

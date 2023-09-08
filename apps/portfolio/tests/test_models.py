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
        self.user_data_2 = {
            'email': 'test2@example.com',
            'first_name': 'Piter',
            'last_name': 'Parker',
            'role': 'salon',
        }

        self.user_1 = CustomUser.objects.create_user(**self.user_data_1)
        self.user_2 = CustomUser.objects.create_user(**self.user_data_2)

        self.file_content = b"Test file content"
        self.avatar = SimpleUploadedFile("test_file.png", self.file_content, content_type="image/png")

        self.profile_data = {
            'user': self.user_1,
            'avatar': self.avatar,
            'about': 'Test about me',
            'status': 'approved',
        }
        self.profile = Profile.objects.create(**self.profile_data)
        self.profile.salons_and_masters.add(self.user_2)

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
        self.assertEqual(self.photo.photo, f'portfolio/photo/{self.post_photo.name}')

    def test_post_creation(self):
        self.assertEqual(self.post.profile, self.profile)
        self.assertEqual(self.post.description, 'Test post description')
        self.assertEqual(self.post.work_type, self.work_type)

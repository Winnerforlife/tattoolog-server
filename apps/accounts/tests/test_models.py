from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.accounts.models import CustomUser, Profile


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

    def test_create_user(self):
        user = CustomUser.objects.create_user(**self.user_data_1)
        self.assertEqual(user.email, self.user_data_1['email'])
        self.assertEqual(user.first_name, self.user_data_1['first_name'])
        self.assertEqual(user.last_name, self.user_data_1['last_name'])
        self.assertEqual(user.role, self.user_data_1['role'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(**self.user_data_2, password='superpassword')
        self.assertEqual(superuser.email, self.user_data_2['email'])
        self.assertEqual(superuser.first_name, self.user_data_2['first_name'])
        self.assertEqual(superuser.last_name, self.user_data_2['last_name'])
        self.assertEqual(superuser.role, self.user_data_2['role'])
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    def test_profile_creation(self):
        file_content = b"Test file content"
        avatar = SimpleUploadedFile("test_file.png", file_content, content_type="image/png")
        user1 = CustomUser.objects.create_user(**self.user_data_1)
        user2 = CustomUser.objects.create_user(**self.user_data_2)

        profile = Profile.objects.create(
            user=user1,
            avatar=avatar,
            about="Test about me",
            status='approved',
        )
        profile.salons_and_masters.add(user2),

        self.assertEqual(profile.avatar.read(), file_content)
        self.assertEqual(profile.about, "Test about me")
        self.assertEqual(profile.status, 'approved')
        self.assertNotEqual(profile.status, 'pending')
        self.assertEqual(profile.salons_and_masters.count(), 1)

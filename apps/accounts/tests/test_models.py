from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import CustomUser, Profile

from cities_light.models import Country, City


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
        self.user_data_3 = {
            'email': 'test3@example.com',
            'first_name': 'Piter3',
            'last_name': 'Parker3',
            'role': 'salon',
        }

        self.user1 = CustomUser.objects.create_user(**self.user_data_1)
        self.user2 = CustomUser.objects.create_user(**self.user_data_2)

        self.country = Country.objects.create(name='United States')
        self.city = City.objects.create(name='New York', country=self.country)

    def test_create_user(self):
        user = self.user1
        self.assertEqual(user.email, self.user_data_1['email'])
        self.assertEqual(user.first_name, self.user_data_1['first_name'])
        self.assertEqual(user.last_name, self.user_data_1['last_name'])
        self.assertEqual(user.role, self.user_data_1['role'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(**self.user_data_3, password='superpassword')
        self.assertEqual(superuser.email, self.user_data_3['email'])
        self.assertEqual(superuser.first_name, self.user_data_3['first_name'])
        self.assertEqual(superuser.last_name, self.user_data_3['last_name'])
        self.assertEqual(superuser.role, self.user_data_3['role'])
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    """
    When creating a CustomUser object:
        - A profile is automatically created.
    """
    def test_profile(self):
        file_content = b"Test file content"
        avatar = SimpleUploadedFile("test_file.png", file_content, content_type="image/png")

        profile = Profile.objects.get(user=self.user1)
        profile.avatar = avatar
        profile.salons_and_masters.add(self.user2),
        profile.about = 'Test about me'
        profile.address = '1-st street 12/45'
        profile.birthday = timezone.datetime(1990, 1, 1).date()
        profile.phone_number = '+48123456789'

        self.assertEqual(profile.avatar.read(), file_content)
        self.assertEqual(profile.salons_and_masters.count(), 1)
        self.assertEqual(profile.about, 'Test about me')

        self.assertEqual(profile.status, 'pending')
        profile.status = 'approved'
        self.assertEqual(profile.status, 'approved')
        self.assertNotEqual(profile.status, 'pending')

        self.assertEqual(profile.country, None)
        self.assertEqual(profile.city, None)
        profile.country = self.country
        profile.city = self.city
        self.assertEqual(profile.country, self.country)
        self.assertEqual(profile.city, self.city)

        self.assertEqual(profile.address, '1-st street 12/45')
        self.assertEqual(str(profile.birthday), '1990-01-01')
        self.assertEqual(profile.phone_number, '+48123456789')

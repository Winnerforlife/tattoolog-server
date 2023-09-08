from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.accounts.models import CustomUser, Profile
from apps.tools.models import SocialMediaType, SocialMedia


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

        self.social_media_type = SocialMediaType.objects.create(name='Facebook')

    def test_social_media_creation(self):
        social_media = SocialMedia.objects.create(
            profile=self.profile,
            social_media_type=self.social_media_type,
            link='https://www.facebook.com/testuser',
        )
        self.assertEqual(social_media.profile, self.profile)
        self.assertEqual(social_media.social_media_type, self.social_media_type)
        self.assertEqual(social_media.link, 'https://www.facebook.com/testuser')

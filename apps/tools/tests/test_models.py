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
        self.user_1 = CustomUser.objects.create_user(**self.user_data_1)
        self.profile_1 = Profile.objects.get(user=self.user_1)

        self.social_media_type = SocialMediaType.objects.create(name='Facebook')

    def test_social_media_creation(self):
        social_media_1 = SocialMedia.objects.create(
            profile=self.profile_1,
            social_media_type=self.social_media_type,
            link='https://www.facebook.com/testuser',
        )
        self.assertEqual(social_media_1.profile, self.profile_1)
        self.assertEqual(social_media_1.social_media_type, self.social_media_type)
        self.assertEqual(social_media_1.link, 'https://www.facebook.com/testuser')

        user_data_2 = {
            'email': 'test2@example.com',
            'first_name': 'Piter',
            'last_name': 'Parker',
            'role': 'salon',
        }
        user_2 = CustomUser.objects.create_user(**user_data_2)
        profile_2 = Profile.objects.get(user=user_2)

        social_media = SocialMedia.objects.filter(profile=profile_2)
        self.assertEqual(social_media.count(), 1)

        SocialMediaType.objects.create(name='Instagram')
        social_media_count = SocialMedia.objects.filter(profile=profile_2).count()
        self.assertEqual(social_media_count, 2)

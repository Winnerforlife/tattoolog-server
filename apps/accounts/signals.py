from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import Profile, CustomUser
from apps.tools.models import SocialMediaType, SocialMedia


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        existing_media_types = SocialMediaType.objects.all()

        for media_type in existing_media_types:
            SocialMedia.objects.create(profile=profile, social_media_type=media_type)


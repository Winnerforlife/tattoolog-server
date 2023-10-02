from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import Profile
from apps.tools.models import SocialMediaType, SocialMedia


@receiver(post_save, sender=SocialMediaType)
def create_social_media_for_profiles(sender, instance, created, **kwargs):
    if created:
        profiles = Profile.objects.all()
        for profile in profiles:
            SocialMedia.objects.create(
                profile=profile,
                social_media_type=instance,
                link=None,
            )

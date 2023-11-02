from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import Profile
from apps.tools.models import SocialMediaType, SocialMedia, Partners, Blog
from apps.tools.utils import convert_to_webp_signal


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


@receiver(post_save, sender=Partners)
def partners_receiver(sender, instance, **kwargs):
    convert_to_webp_signal('logo')(sender, instance, **kwargs)


@receiver(post_save, sender=Blog)
def blog_receiver(sender, instance, **kwargs):
    convert_to_webp_signal('image')(sender, instance, **kwargs)

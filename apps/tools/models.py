from django.db import models
from django.utils.translation import gettext_lazy as _


class SocialMedia(models.Model):
    profile = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='social_media_profile',
    )
    social_media_type = models.ForeignKey(
        'tools.SocialMediaType',
        on_delete=models.CASCADE,
        related_name='social_media_type',
    )
    link = models.URLField(_('Social media link'))

    def __str__(self):
        return f"{self.profile.user.get_username()} - {self.social_media_type.name}"


class SocialMediaType(models.Model):
    name = models.CharField(_('Social media name'), max_length=32)

    def __str__(self):
        return self.name

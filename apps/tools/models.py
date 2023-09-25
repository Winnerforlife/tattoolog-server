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
    link = models.URLField(_('Social media link'), null=True, blank=True)

    def __str__(self):
        return f"{self.profile.user.get_full_name()} - {self.social_media_type.name}"


class SocialMediaType(models.Model):
    name = models.CharField(_('Social media name'), max_length=32)

    def __str__(self):
        return self.name


class Partners(models.Model):
    name = models.CharField(_('Partner name'), max_length=128)
    logo = models.ImageField(_('Logo'), upload_to="partners/logo")
    link = models.URLField(_('Partner link'), null=True, blank=True)

    def __str__(self):
        return self.name

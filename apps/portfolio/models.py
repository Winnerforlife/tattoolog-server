from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    profile = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='post_profile',
    )
    description = models.TextField(_("Description"), default='', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    work_type = models.ForeignKey(
        'portfolio.WorkType',
        on_delete=models.SET_NULL,
        related_name='post_work_type',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"({self.profile.user.get_full_name()}) postID-{self.id}"


class Photo(models.Model):
    post = models.ForeignKey(
        'portfolio.Post',
        on_delete=models.CASCADE,
        related_name='photo_post',
    )
    photo = models.ImageField(_("Post photo"), upload_to="portfolio/photo")


class WorkType(models.Model):
    name = models.CharField(_("Work type name"), default='', max_length=32)
    description = models.TextField(_("Description"), default='', blank=True)

    def __str__(self):
        return self.name

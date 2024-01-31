from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.tools.choices import STATUS_CHOICES, WORK_TYPE_CATEGORY_CHOICE


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
    category = models.CharField(
        _("Work type category"),
        choices=WORK_TYPE_CATEGORY_CHOICE,
        default=WORK_TYPE_CATEGORY_CHOICE.tattoo
    )

    def __str__(self):
        return self.name


class ModerationAssociation(models.Model):
    profile = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='moderation_profile_associate',
    )
    type = models.ForeignKey(
        'tools.AssociationType',
        on_delete=models.CASCADE,
        related_name='association_type',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Status of consideration of the association's label"
    )
    comment = models.TextField(_("Comment"), default='', blank=True)

    def __str__(self):
        return f"({self.profile.user.get_full_name()}) {self.type.name} - {self.status}"


class AssociationPhotoProof(models.Model):
    moderation = models.ForeignKey(
        'portfolio.ModerationAssociation',
        on_delete=models.CASCADE,
        related_name='photo_proof_moderation',
    )
    photo = models.ImageField(_("Association photo proof"), upload_to="proof/photo")


class ModerationFromProject(models.Model):
    profile = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='moderation_profile_from_project',
    )
    type = models.ForeignKey(
        'tools.Project',
        on_delete=models.CASCADE,
        related_name='project_type',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Status of consideration"
    )
    comment = models.TextField(_("Comment"), default='', blank=True)

    def __str__(self):
        return f"({self.profile.user.get_full_name()}) {self.type.name} - {self.status}"

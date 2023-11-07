from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


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


class Blog(models.Model):
    image = models.ImageField(
        _('Image'),
        upload_to='blog_images/',
        help_text="Image to be displayed in the blog post body, card photo and opengraph image"
    )
    title = models.CharField(_('Blog title'), max_length=255)
    body = models.TextField(_('Blog body'))
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.CharField(
        _('Slug'),
        max_length=32,
        help_text="Page name in url. Example: https://domain.com/blog/[my_slug]/"
    )
    meta_title_tag = models.CharField(
        _('Meta title tag'),
        max_length=255,
        help_text="Clickable page title displayed in search engine results as a headline"
    )
    meta_description = models.CharField(
        _('Meta description'),
        max_length=255,
        help_text="Description displayed beneath the headline in search engine results"
    )
    meta_keywords = models.CharField(
        _('Meta keywords'),
        max_length=255,
        help_text="List of keywords that correspond to the content of a website page"
    )
    opengraph_title = models.CharField(
        _('Opengraph title'),
        max_length=255,
        help_text="The title of your object as it should appear within the graph"
    )
    opengraph_description = models.CharField(
        _('Opengraph description'),
        max_length=255,
        help_text="A one to two sentence description of your object"
    )

    def __str__(self):
        return self.title


class Rating(models.Model):
    profile = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        related_name='rating_profile',
    )
    mark = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(default='', blank=True)

    def __str__(self):
        return f"{self.profile.user.get_full_name()}_{self.mark}"


class Festival(models.Model):
    image = models.ImageField(
        _('Image'),
        upload_to='festival_images/',
        help_text="Image to be displayed in the festival post body, card photo and opengraph image"
    )
    title = models.CharField(_('Festival title'), max_length=255)
    about = models.TextField(_('About festival'))
    rules = models.TextField(_('Festival rules'), default="", blank=True)
    slug = models.CharField(
        _('Slug'),
        max_length=32,
        help_text="Page name in url. Example: https://domain.com/festival/[my_slug]/"
    )
    date_end = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    form_url = models.URLField(_("Link to registration form"))

    def __str__(self):
        return self.title

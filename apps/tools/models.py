from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from ckeditor.fields import RichTextField

from apps.tools.choices import LANGUAGE_CHOICE, COUNTRY_CHOICE, PARTNER_TYPE_CHOICE


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
    link = models.CharField(_('Social media link'), null=True, blank=True)

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
    type = models.CharField(max_length=10, choices=PARTNER_TYPE_CHOICE, default='project')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")


class BlogPost(models.Model):
    image = models.ImageField(
        _('Image'),
        upload_to='blog_images/',
        help_text="Image to be displayed in the blog post body and card photo",
        null=True,
        blank=True
    )
    category = models.ManyToManyField(
        'tools.BlogCategory',
        related_name='blog_category',
        verbose_name=_("Blog category"),
        blank=True
    )
    title = models.CharField(_('Blog post title'), max_length=255)
    slug = models.CharField(
        _('Slug'),
        max_length=32,
        help_text="Page name in url. Example: https://domain.com/blog/[my_slug]/"
    )
    created_at = models.DateTimeField(default=timezone.now)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICE, default='en')
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICE, default='pl')
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.title} (country: {self.country}) (language: {self.language}) (slug: {self.slug})"


class BlogBody(models.Model):
    post = models.ForeignKey(
        'tools.BlogPost',
        on_delete=models.CASCADE,
        related_name='blog_body',
    )
    title = models.CharField(_('Blog body title'), max_length=255)
    body = RichTextField(_('Blog body'))


class BlogBodyPhoto(models.Model):
    post = models.ForeignKey(
        'tools.BlogBody',
        on_delete=models.CASCADE,
        related_name='blog_body_photo',
    )
    photo = models.ImageField(_("Blog photo"), upload_to="blog_body/photo", null=True, blank=True)
    alt_name = models.CharField(
        _('Photo ALT name'),
        max_length=255,
        help_text="ALT name for photo",
        null=True,
        blank=True
    )


class BlogMeta(models.Model):
    post = models.OneToOneField(
        'tools.BlogPost',
        on_delete=models.CASCADE,
        related_name='blog_meta',
    )
    meta_title_tag = models.CharField(
        _('Meta title tag'),
        max_length=255,
        help_text="Clickable page title displayed in search engine results as a headline",
        null=True,
        blank=True
    )
    meta_description = models.CharField(
        _('Meta description'),
        max_length=255,
        help_text="Description displayed beneath the headline in search engine results",
        null=True,
        blank=True
    )
    meta_keywords = models.CharField(
        _('Meta keywords'),
        max_length=255,
        help_text="List of keywords that correspond to the content of a website page",
        null=True,
        blank=True
    )
    opengraph_title = models.CharField(
        _('Opengraph title'),
        max_length=255,
        help_text="The title of your object as it should appear within the graph",
        null=True,
        blank=True
    )
    opengraph_description = models.CharField(
        _('Opengraph description'),
        max_length=255,
        help_text="A one to two sentence description of your object",
        null=True,
        blank=True
    )
    opengraph_image = models.ImageField(
        _('Opengraph image'),
        upload_to='opengraph_images/',
        help_text="Image to be displayed on the opengraph image",
        null=True,
        blank=True
    )


class BlogPhotoCarousel(models.Model):
    post = models.ForeignKey(
        'tools.BlogPost',
        on_delete=models.CASCADE,
        related_name='blog_photo_carousel',
    )
    photo = models.ImageField(_("Photo carousel"), upload_to="blog_carousel/photo", null=True, blank=True)


class BlogCategory(models.Model):
    name = models.CharField(_('Blog category name'), max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Blog category")
        verbose_name_plural = _("Blog categories")


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


class AssociationType(models.Model):
    name = models.CharField(_('Association name'), max_length=128)
    link = models.URLField(_('Association link'), null=True, blank=True)

    def __str__(self):
        return self.name


class Festival(models.Model):
    image = models.ImageField(
        _('Image'),
        upload_to='festival_images/',
        help_text="Image to be displayed in the festival post body, card photo and opengraph image",
        null=True,
        blank=True
    )
    title = models.CharField(_('Festival title'), max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        'tools.FestivalCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='festival_category',
    )
    about = RichTextField(_('About festival'), blank=True, null=True)
    rules = RichTextField(_('Festival rules'), default="", blank=True)
    slug = models.CharField(
        _('Slug'),
        max_length=32,
        help_text="Page name in url. Example: https://domain.com/festival/[my_slug]/"
    )
    date_end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    form_url = models.URLField(_("Link to registration form"), blank=True, null=True)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICE, default='pl')

    def __str__(self):
        return f"{self.title} - {self.country}"


class FestivalCategory(models.Model):
    name = models.CharField(_('Festival category name'), max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Festival category")
        verbose_name_plural = _("Festival categories")

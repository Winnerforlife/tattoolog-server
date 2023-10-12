from django.db.models import Avg
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.accounts.managers import CustomUserManager
from apps.tools.models import Rating


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('master', 'Mater'),
        ('salon', 'Salon'),
    )
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email


class Profile(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('canceled', 'Canceled'),
    )
    user = models.OneToOneField(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True
    )
    avatar = models.ImageField(_("Avatar"), upload_to="users/avatars", null=True, blank=True)
    count_visit = models.PositiveSmallIntegerField(_('Count visit'), default=0)
    salons_and_masters = models.ManyToManyField(
        'accounts.CustomUser',
        related_name='profile_salons_and_masters',
        verbose_name=_("Salons/Masters"),
        blank=True
    )
    about = models.TextField(_("About me"), default='', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(default="", blank=True, max_length=255)
    birthday = models.DateField(_('Birthday'), null=True, blank=True)
    phone_number = PhoneNumberField(blank=True)

    def get_average_rating(self):
        average_rating = Rating.objects.filter(profile=self.user.id).aggregate(Avg('mark'))['mark__avg']
        if average_rating is not None:
            return round(average_rating, 1)
        return 0

    def __str__(self):
        return self.user.get_full_name()

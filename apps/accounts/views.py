import random
import string
import logging
from datetime import datetime
from cities_light.models import Country, City
from django.db.models.functions import Coalesce
from django.db.models import Avg, Count, FloatField
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.accounts.filters import ProfileFilter
from apps.accounts.models import Profile, CustomUser
from apps.accounts.serializers import ProfileSerializer, ProfileFilterSerializer, CRMIntegrationProfiles, \
    TransferActivationEmailSerializer
from apps.portfolio.models import Post, Photo
from apps.tools.models import SocialMedia
from apps.tools.utils import CustomPagination, send_sms

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class IsAuthenticatedOrPatch(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PATCH':
            return IsAuthenticated().has_permission(request, view)
        return True


@extend_schema(
    description=(
            'Field "user" represents the profile ID because the Profile model uses CustomUser model'
            ' as the primary key for a one-to-one relationship.'
    )
)
class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticatedOrPatch]
    http_method_names = ['get', 'patch']

    def retrieve_profile(self, request, *args, **kwargs):
        instance = self.get_object()
        current_user = request.user
        if request.method == 'GET' and instance.user != current_user:
            instance.count_visit += 1
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve_profile(request, *args, **kwargs)
        return super().retrieve(request, *args, **kwargs)


@extend_schema(
    summary='Retrieving all profiles of a specific role. (Default pagination size 10 objects)',
    description=(
            'Using optional parameters you can filter the final result:\n'
            '* city - filters by the field city.\n'
            '* country - filters by the field country.\n'
            '* mentor - filters by the field mentor.\n'
            '* name - filters by the fields first_name and last_name.\n'
            '* open_to_work - filters by the field open_to_work.\n'
            '* rating_order - filters by rating [params: acs, desc].\n'
            '* relocate - filters by the field relocate.\n'
            '* work_type - filters by the field work_type by name object.'
    )
)
class ProfileApiView(ListAPIView):
    serializer_class = ProfileFilterSerializer
    permission_classes = [AllowAny]
    filterset_class = ProfileFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Profile.objects.none()
        role = self.kwargs['role']

        queryset = Profile.objects.filter(user__role=role, status='approved').annotate(
            avg_rating=Coalesce(Avg('rating_profile__mark'), 0, output_field=FloatField()),
            rating_count=Count('rating_profile'),
            post_count=Count('post_profile')
        ).order_by('-post_count')

        return queryset


@extend_schema(
    summary='Retrieving all profiles for CRM integration.',
    description=(
            'Using optional parameter: **date**. You can filter the final result.\n'
            '* date - Filters profiles created later than the entered date. (%Y-%m-%d)'
    )
)
class CRMIntegrationProfilesAPIView(ListAPIView):
    serializer_class = CRMIntegrationProfiles
    permission_classes = [AllowAny]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Profile.objects.none()
        date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d')
        return Profile.objects.filter(user__date_joined__gte=date)


def get_object_or_none(klass, *args, **kwargs):
    try:
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        return None


@extend_schema(
    summary='Creating a new user from CRM and sending an activation email or sms.',
)
class TransferActivationEmailView(CreateAPIView):
    serializer_class = TransferActivationEmailSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def generate_password():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            password = self.generate_password()
            user_instance = self.create_user(request, password)
            self.handle_profile_update(request, user_instance)
            self.send_notification(user_instance, password)
            return Response({'status': f'User {user_instance} from CRM created'}, status=status.HTTP_200_OK)

    def create_user(self, request, password):
        try:
            user_data = self.get_user_data(request)
            return CustomUser.objects.create_user(password=password, is_active=False, **user_data)
        except Exception as e:
            logging.error(f"Error creating user: {e}")
            return Response({'error': 'Error creating user'}, status=status.HTTP_400_BAD_REQUEST)

    def get_user_data(self, request):
        logging.info(f"request.data: {request.data}")
        logging.info(f"request.FILES: {request.FILES}")
        email = request.data.get('email')
        logging.info(f"email: {email}")
        phone_number = request.data.get('phone_number')
        logging.info(f"phone_number: {phone_number}")
        return {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'role': request.data.get('role'),
            'email': email,
            'phone_number': phone_number,
            'username': email if email else phone_number,
        }

    def handle_profile_update(self, request, user_instance):
        profile_instance = Profile.objects.get(user=user_instance)
        logging.info(f"profile_instance: {profile_instance}")

        profile_instance.status = 'approved'
        profile_instance.about = request.data.get('about')
        logging.info(f"profile_instance.about: {profile_instance.about}")
        profile_instance.country = get_object_or_none(Country, name=request.data.get('country'))
        logging.info(f"profile_instance.country: {profile_instance.country}")
        profile_instance.city = get_object_or_none(City, name=request.data.get('city'))
        logging.info(f"profile_instance.city: {profile_instance.city}")
        profile_instance.avatar = request.FILES.get('avatar') if 'avatar' in request.FILES else None
        logging.info(f"profile_instance.avatar: {profile_instance.avatar}")
        profile_instance.save()

        social_media_instance = SocialMedia.objects.get(profile=profile_instance, social_media_type__name="Instagram")
        social_media_instance.link = request.data.get('social_link')
        social_media_instance.save()

        work_photos = request.FILES.getlist('work_photos')
        logging.info(f"work_photos: {work_photos}")
        if work_photos:
            for photo_file in work_photos:
                post_instance = Post.objects.create(profile=profile_instance)
                Photo.objects.create(post=post_instance, photo=photo_file)

    def send_notification(self, user_instance, password):
        if user_instance.email:
            self.send_activation_email(user_instance, password)
        else:
            self.send_activation_sms(user_instance, password)

    def prepare_email_context(self, request, user_instance, password):
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user_instance.id))
        token = default_token_generator.make_token(user_instance)
        return {
            'protocol': 'https',
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
            'customer_username': user_instance.username,
            'customer_password': password,
            'url': f"activation/{uid}/{token}/",
        }

    def send_activation_email(self, user_instance, password):
        try:
            email_context = self.prepare_email_context(self.request, user_instance, password)
            subject = f'Account activation on {email_context["domain"]}'
            email_html_message = render_to_string('email/transfer_crm_activation.html', email_context)
            send_mail(subject, '', '', [user_instance.email], html_message=email_html_message)
        except Exception as e:
            logging.error(f"Error sending activation email: {e}")

    def send_activation_sms(self, user_instance, password):
        logging.info(f"Sent activation sms")
        uid = urlsafe_base64_encode(force_bytes(user_instance.id))
        token = default_token_generator.make_token(user_instance)
        message = (f"Hi!💜\n\n"
                   f"login: {str(user_instance.phone_number)}\n"
                   f"password: {password}\n\n"
                   f"Link to log into the catalog:\n\n"
                   f"https://tattoolog.pl/activation/{uid}/{token}/")
        send_sms(str(user_instance.phone_number), message)

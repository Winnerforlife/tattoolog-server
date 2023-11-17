import random
import string
import logging
from datetime import datetime
from cities_light.models import Country, City

from django.db.models import Avg, Count, F
from django.db import transaction
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.accounts.filters import ProfileFilter
from apps.accounts.models import Profile, CustomUser
from apps.accounts.serializers import ProfileSerializer, ProfileFilterSerializer, CRMIntegrationProfiles, \
    TransferActivationEmailSerializer
from apps.portfolio.models import Post, Photo
from apps.tools.models import SocialMedia
from apps.tools.utils import CustomPagination

logger = logging.getLogger(__name__)


@extend_schema(
    description=(
            'Field "user" represents the profile ID because the Profile model uses CustomUser model'
            ' as the primary key for a one-to-one relationship.'
    )
)
class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]

    # ToDo убрать ненужные ендпоинты
    # http_method_names = ['get', 'patch']

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
            'Using optional parameters: **name**, **city**, **country**. You can filter the final result.\n'
            '* name - filters by the fields first_name and last_name.\n'
            '* city - filters by the field city.\n'
            '* country - filters by the field country.'
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

        queryset = Profile.objects.filter(user__role=role).annotate(
            avg_rating=Avg('rating_profile__mark'),
            rating_count=Count('rating_profile')
        )
        queryset = queryset.order_by(F('avg_rating').desc(nulls_last=True), F('rating_count').desc(nulls_last=True))

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
            logger.error(f"Error creating user: {e}")
            return Response({'error': 'Error creating user'}, status=status.HTTP_400_BAD_REQUEST)

    def get_user_data(self, request):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        return {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'role': request.data.get('role'),
            'email': email,
            'phone_number': phone_number,
            'username': email if email else phone_number,
        }

    def handle_profile_update(self, request, user_instance):
        try:
            profile_instance = Profile.objects.get(user=user_instance)

            profile_instance.status = 'approved'
            profile_instance.about = request.data.get('about')
            profile_instance.country = Country.objects.get(name=request.data.get('country')) if request.data.get('country') else None
            profile_instance.city = City.objects.get(name=request.data.get('city')) if request.data.get('city') else None
            profile_instance.avatar = request.FILES.get('avatar')
            profile_instance.save()

            social_media_instance = SocialMedia.objects.get(profile=profile_instance, social_media_type__name="Instagram")
            social_media_instance.link = request.data.get('social_link')
            social_media_instance.save()

            work_photos = request.FILES.getlist('work_photos')
            for photo_file in work_photos:
                post_instance = Post.objects.create(profile=profile_instance)
                Photo.objects.create(post=post_instance, photo=photo_file)
        except ObjectDoesNotExist as e:
            logger.warning(f"Object not found: {e}")

    def send_notification(self, user_instance, password):
        if user_instance.email:
            self.send_activation_email(user_instance, password)
        else:
            self.send_activation_sms()

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
            logger.error(f"Error sending activation email: {e}")

    # TODO Реализация отправки сообщения в sms
    def send_activation_sms(self):
        logger.info(f"Sent activation sms")

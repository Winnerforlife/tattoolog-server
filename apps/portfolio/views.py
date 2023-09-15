from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from apps.portfolio.models import Post, Photo, WorkType
from apps.portfolio.serializers import PostSerializer, PostCreateSerializer, PhotoCreateSerializer, WorkTypeSerializer


@extend_schema(summary='Create post for specific user profile.')
class PostCreateApiView(CreateAPIView):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]


@extend_schema(summary='Create photos for specific post.')
class PhotoCreateView(CreateAPIView):
    serializer_class = PhotoCreateSerializer
    queryset = Photo.objects.all()
    permission_classes = [AllowAny]


@extend_schema(summary='Retrieving work types.')
class WorkTypeApiView(ListAPIView):
    serializer_class = WorkTypeSerializer
    queryset = WorkType.objects.all()
    permission_classes = [AllowAny]


@extend_schema(summary='Retrieving all posts of a specific user.')
class ProfilePostsApiView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Post.objects.none()
        user_id = self.kwargs['user_id']
        return Post.objects.filter(profile__user__id=user_id)

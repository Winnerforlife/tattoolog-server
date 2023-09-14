from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from apps.portfolio.models import Post
from apps.portfolio.serializers import PostSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)


@extend_schema(summary='Retrieving all posts of a specific user.')
class ProfilePostsApiView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Post.objects.none()
        user_id = self.kwargs['user_id']
        return Post.objects.filter(profile__user__id=user_id)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from apps.portfolio.models import Post
from apps.portfolio.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]


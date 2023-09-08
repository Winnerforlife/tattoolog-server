from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from apps.portfolio.models import Post
from apps.portfolio.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]


class ProfilePostsApiView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.objects.filter(profile__user__id=user_id)

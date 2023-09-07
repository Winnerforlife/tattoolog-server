from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.portfolio.models import Post
from apps.portfolio.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({"status": status.HTTP_201_CREATED})

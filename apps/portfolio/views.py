from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.portfolio.models import Post, Photo, WorkType, AssociationPhotoProof, ModerationAssociation
from apps.portfolio.serializers import (PostSerializer, PostCreateSerializer, PhotoCreateSerializer, WorkTypeSerializer,
                                        AssociationPhotoProofSerializer, ModerationAssociationSerializer)

from apps.tools.utils import CustomPagination


@extend_schema(summary='Create post for specific user profile.')
class PostCreateApiView(CreateAPIView):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]


@extend_schema(summary='Create photos for specific post.')
class PhotoCreateView(CreateAPIView):
    serializer_class = PhotoCreateSerializer
    queryset = Photo.objects.all()
    permission_classes = [IsAuthenticated]


@extend_schema(summary='Retrieving work types.')
class WorkTypeApiView(ListAPIView):
    serializer_class = WorkTypeSerializer
    queryset = WorkType.objects.all()
    permission_classes = [AllowAny]


@extend_schema(summary='Retrieving all posts of a specific user.')
class ProfilePostsApiView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Post.objects.none()
        user_id = self.kwargs['user_id']
        return Post.objects.filter(profile__user__id=user_id)


@extend_schema(summary='Retrieving specific post by id.')
class PostApiView(RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]


@extend_schema(
    summary='Create photo proofs for specific association.',
    description=(
        '* photos - (Array of photos to be attached for moderation).\n'
        '* moderation - {moderation id} (The users moderation id. Returned when the moderation is created).'
    )
)
class AssociationPhotoProofCreateView(CreateAPIView):
    serializer_class = AssociationPhotoProofSerializer
    queryset = AssociationPhotoProof.objects.all()
    permission_classes = [IsAuthenticated]


@extend_schema(
    summary='Create request for moderation association.',
    description=(
        '* profile - {profile id} (The user who applied).\n'
        '* type - {type id} (Type of association label. "/tools/association-type/").\n'
        '* status - {**pending**/approved/canceled} (Moderation status of the application. default=pending).\n'
        '* comment - {string} (User comments to the moderation request).'
    )
)
class ModerationAssociationCreateView(CreateAPIView):
    serializer_class = ModerationAssociationSerializer
    queryset = ModerationAssociation.objects.all()
    permission_classes = [IsAuthenticated]

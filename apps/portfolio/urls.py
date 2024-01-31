from django.urls import path

from apps.portfolio.views import PostCreateApiView, ProfilePostsApiView, PhotoCreateView, WorkTypeApiView, \
    AssociationPhotoProofCreateView, ModerationAssociationCreateView, PostApiView, ModerationFromProjectCreateView

urlpatterns = [
    path('posts/profile/<int:user_id>/', ProfilePostsApiView.as_view(), name='user-posts-list'),
    path('post/<int:pk>/', PostApiView.as_view(), name='retrieve-post'),
    path('post-photo/create/', PhotoCreateView.as_view(), name='post-photo'),
    path('post/create/', PostCreateApiView.as_view(), name='post'),
    path('work_types/', WorkTypeApiView.as_view(), name='work_types'),
    path('moderation-association/create/', ModerationAssociationCreateView.as_view(), name='moderation-association'),
    path('moderation-from-project/create/', ModerationFromProjectCreateView.as_view(), name='moderation-from-project'),
    path('association-photo-proof/create/', AssociationPhotoProofCreateView.as_view(), name='association-photo-proof'),
]

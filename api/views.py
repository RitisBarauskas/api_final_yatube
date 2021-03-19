from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from api.models import Group, Post, User

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer,
    UserSerializer)

PERMISSION_CLASSES = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = PERMISSION_CLASSES


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = PERMISSION_CLASSES

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = PERMISSION_CLASSES

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = PERMISSION_CLASSES
    http_method_names = ('get', 'post')


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer
    http_method_names = ('get', 'post')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=user__username', '=following__username')

    def get_queryset(self):
        user = self.request.user
        return user.following.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

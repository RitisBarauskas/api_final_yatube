from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet,
                    UserViewSet)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet, basename='comment')
router_v1.register('posts', PostViewSet, basename='post')
router_v1.register('group', GroupViewSet, basename='group')
router_v1.register('follow', FollowViewSet, basename='follow')

urlpatterns = [path('', include(router_v1.urls)),
               path('token/',
                    TokenObtainPairView.as_view(),
                    name='token_obtain_pair'),
               path('token/refresh/',
                    TokenRefreshView.as_view(),
                    name='token_refresh'), ]

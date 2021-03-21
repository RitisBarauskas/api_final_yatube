from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet,
                    UserViewSet)

router_v1 = DefaultRouter()
router_v1.register('v1/users', UserViewSet, basename='user')
router_v1.register(r'v1/posts/(?P<post_id>\d+)/comments',
                   CommentViewSet, basename='comment')
router_v1.register('v1/posts', PostViewSet, basename='post')
router_v1.register('v1/group', GroupViewSet, basename='group')
router_v1.register('v1/follow', FollowViewSet, basename='follow')

urlpatterns = [path('', include(router_v1.urls)),
               path('v1/token/',
                    TokenObtainPairView.as_view(),
                    name='token_obtain_pair'),
               path('v1/token/refresh/',
                    TokenRefreshView.as_view(),
                    name='token_refresh'), ]

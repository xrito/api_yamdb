from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (TitleViewSet, GenreViewSet, CategoryViewSet,
                       ReviewViewSet, CommentViewSet, UserViewSet)

router = SimpleRouter()
router.register('titles', TitleViewSet)
# router.register('genres', GenreViewSet)
# router.register('categories', CategoryViewSet)
# router.register('users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/signup/',),
    # path('v1/auth/token/',),
    # path('v1/users/me/',)
]

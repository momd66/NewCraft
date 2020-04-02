from django.urls import path

from .views import PostListRecommended,FollowedPosts

urlpatterns = [
    path('', PostListRecommended.as_view(),name='home'),
    path('following/', FollowedPosts.as_view(),name="following-list"),
]

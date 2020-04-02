from django.urls import path

from .views import (
	RegisterView,
	LoginView,
	profile,
	UpdateProfile,
	ProfileUpdate,
	ProfileDetail,
	AddLike,
	APIAddLike,
	AddComment,
	AddLikeComment,
	APIAddLikeComment,
	AddReply,
	APIAddLikeReply,
	LoadMorePost,
	LoadMorePostHome,
	AddToRecommendition,
	APIFollow,
	LoadMorePostFollwings,
	LoadMoreUserPosts,
	LoadMoreComments,
	LoadMoreReplies
	)

from General.views import LoadMoreSearchedPosts,LoadMoreProfiles

from django.contrib.auth import views as auth_views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegisterView,name='register'),
    path('login/', LoginView,name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="logout.html"),name="logout"),
    path('profile/', profile,name="profile"),
    path('profile/update/', UpdateProfile,name="update-profile"),
    path('update/profile/',ProfileUpdate.as_view(),name='profile-update'),
    path('user/<str:slug>/',ProfileDetail.as_view(),name='user-detail'),


    path('post/<str:slug>/addlike/',AddLike.as_view(),name='add-like'),
    path('post/<str:slug>/addlike/api/',APIAddLike.as_view(),name='add-like-api'),\
    path('post/<str:slug>/recommend/api/',AddToRecommendition.as_view(),name='recommend'),

    path('post/<str:slug>/addcomment/',AddComment.as_view(),name="add-comment"),
    path('comment/<str:slug>/reply/',AddReply.as_view(),name="add-reply"),

    path('comment/<str:slug>/addlike/',AddLikeComment.as_view(),name='add-like-comment'),
    path('comment/<str:slug>/addlike/api/',APIAddLikeComment.as_view(),name='add-like-comment-api'),

    path('reply/<int:id>/addlike/api/',APIAddLikeReply.as_view(),name='add-like-reply-api'),

    path('user/<str:slug>/loadmorepost/',LoadMorePost.as_view(),name='load-more-post'),
    path('user/<str:slug>/follow/api/',APIFollow.as_view(),name='follow-api'),
    path('loadmoreposts/',LoadMorePostHome.as_view(),name='load-more-post-home'),
    path('loadmorepostsfollowings/',LoadMorePostFollwings.as_view(),name='load-more-post-followings'),
    path('loadmorepostsuser/<str:slug>/',LoadMoreUserPosts.as_view(),name='load-more-post-user'),
    path('loadmorecommentspost/<str:slug>/',LoadMoreComments.as_view(),name='load-more-comments-post'),
    path('loadmorerepliescomment/<str:slug>/',LoadMoreReplies.as_view(),name='load-more-replies-comment'),

    path('loadmorepostsSaerch/',LoadMoreSearchedPosts.as_view(),name='load-more-post-search'),
    path('loadmoreprofiles/',LoadMoreProfiles.as_view(),name='load-more-profiles'),



    

]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
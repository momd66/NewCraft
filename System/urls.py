from django.urls import path

from .views import (
	RegisterView,
	LoginView,
	profile,
	UpdateProfile,
	ProfileUpdate,
	ProfileDetail,


	SendFriendRequest,
	APISendFriendRequest,
	DeleteFriend,
	APIDeleteFriend,
	AcceptFriendRequest,
	APIAcceptFriendRequest,
	DeleteFriendRequest,
	APIDeleteFriendRequest
	)

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

    path('user/<str:slug>/FriendRequest/',SendFriendRequest.as_view(),name='S-F-request'),
    path('user/<str:slug>/FriendRequest/api/',APISendFriendRequest.as_view(),name='S-F-request-api'),


    path('user/<str:slug>/AcceptRequest/',AcceptFriendRequest.as_view(),name='A-F-request'),
    path('user/<str:slug>/AcceptRequest/api/',APIAcceptFriendRequest.as_view(),name='A-F-request-api'),
    

    path('user/<str:slug>/DeleteRequest/',DeleteFriendRequest.as_view(),name='D-F-request'),
    path('user/<str:slug>/DeleteRequest/api/',APIDeleteFriendRequest.as_view(),name='D-F-request-api'),


    path('user/<str:slug>/DeleteFriend/',DeleteFriend.as_view(),name='D-friend'),
    path('user/<str:slug>/DeleteFriend/api/',APIDeleteFriend.as_view(),name='D-friend-api'),

    

]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
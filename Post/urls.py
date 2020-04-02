from django.urls import path

from .views import (
	PostDetail,
	PostCreate,
	PostUpdate,
	APIDeletePost,
	
	)

urlpatterns = [
    path('post/<str:slug>/', PostDetail.as_view() , name="post-detail"),
    path('post/', PostCreate.as_view(),name="post-create"),
    path("post/<str:slug>/edit/",PostUpdate.as_view(),name="post-update"),
    path("post/<str:slug>/delete/api/",APIDeletePost.as_view(),name="post-delete-api"),


]
from django.urls import path

from .views import (
	CommentDetail,
	APIDeleteComment,
	APIDeleteReply
	)

urlpatterns = [
    path('comment/<str:slug>/', CommentDetail.as_view() , name="comment-detail"),
    path("comment/<str:slug>/delete/api/",APIDeleteComment.as_view(),name="comment-delete-api"),
    path("reply/<int:id>/delete/api/",APIDeleteReply.as_view(),name="reply-delete-api"),

]
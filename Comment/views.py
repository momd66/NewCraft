from django.shortcuts import render,redirect,get_object_or_404

from .models import Post

from System.models import User

from django.views.generic import (
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	ListView
	)

from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	UserPassesTestMixin
	)

from django.utils import timezone

from Comment.models import Comment,Reply
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
import os

class CommentDetail(DetailView):
	model         = Comment
	template_name = "comment_detail.html"
	context_object_name = 'post'
	comments = ''

	def get(self,request,slug, *args, **kwargs):
		post = Comment.objects.filter(slug=slug).first()
		comments = Reply.objects.filter(comment=post).order_by('timestamp')[:5]
		self.comments = comments

		return super().get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		active = {'ActiveHome':'active2','comments':self.comments}
		context = super().get_context_data(**kwargs)
		context['active'] = active
		return context



class APIDeleteComment(APIView):
	authentication_classes = [authentication.SessionAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request,slug=None, format=None):
		slug = self.kwargs.get('slug')
		user = self.request.user
		comment = get_object_or_404(Comment,slug=slug)
		replies = Reply.objects.filter(comment=comment)
		deleted = False
		if user.is_authenticated:
			if user == comment.user:
				for reply in replies:
					reply.delete()
				comment.delete()

				deleted = True


		data = {"deleted":deleted} 
		return Response(data)


class APIDeleteReply(APIView):
	authentication_classes = [authentication.SessionAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request,id=None, format=None):
		id_ = self.kwargs.get('id')
		user = self.request.user
		reply = get_object_or_404(Reply,id=id_)
		deleted = False
		if user.is_authenticated:
			if user == reply.user:
				reply.delete()
				deleted = True


		data = {"deleted":deleted} 
		return Response(data)
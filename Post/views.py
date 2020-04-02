from django.shortcuts import render,redirect,get_object_or_404

from .models import Post

#from System.models import User

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

from Comment.models import Comment

from Comment.models import Comment,Reply
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
import os
from django.db.models import Case, When
from django.db.models import Count

class PostDetail(DetailView):
	model         = Post
	template_name = "post_detail.html"
	context_object_name = 'post'

	comments = ''
	comments_all = ''

	def get(self,request,slug, *args, **kwargs):
		post = Post.objects.filter(slug=slug).first()
		#comments = Comment.objects.filter(post=post).order_by('-timestamp')[:5]
		ids_at_top = [request.user.id]
		comments = Comment.objects.annotate(like_count=Count('likes')).order_by(Case(When(user__id__in=ids_at_top, then=0), default=1),'-like_count','-timestamp').filter(post=post)[:5]
		comments_all = Comment.objects.filter(post=post).order_by('-timestamp')
		self.comments = comments
		self.comments_all = comments_all

		return super().get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		active = {'ActiveHome':'active2','comments':self.comments,'comments_all':self.comments_all}
		context = super().get_context_data(**kwargs)
		context['active'] = active
		return context

import re

class PostCreate(LoginRequiredMixin,CreateView):
	model = Post
	template_name = "post_form.html"
	fields = ["content","image","privacy"]
	def form_valid(self,form):
		form.instance.author = self.request.user

		if form.instance.privacy == "Private":
			form.instance.draft = True

		elif form.instance.privacy == "Public":
			form.instance.TimeChange += 1
			form.instance.draft = False
		
		content = form.instance.content
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
		

		listToStr = ' '.join([str(elem) for elem in urls])

		text = form.instance.content
		for url in urls:
			text = text.replace(url, "")
		
		form.instance.clean_content = text
		form.instance.links = urls


		form.save()
		return redirect('user-detail',slug=self.request.user.profile.slug)
		

	def get_context_data(self, **kwargs):
		active = {'ActivePost':'active','PostNone':'d-none'}
		context = super().get_context_data(**kwargs)
		context['active'] = active
		return context


class PostUpdate(UserPassesTestMixin,LoginRequiredMixin,UpdateView):
	model = Post
	template_name = "post_update_form.html"
	fields = ["content","privacy"]
	time = timezone.now
	def form_valid(self,form):
		form.instance.author = self.request.user

		if form.instance.privacy == "Private":
			form.instance.draft = True
			
		elif form.instance.privacy == "Public":
			form.instance.draft = False
			if form.instance.TimeChange == 0:
				form.instance.date_posted = timezone.now()
				form.instance.TimeChange += 1


		content = form.instance.content
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
		

		listToStr = ' '.join([str(elem) for elem in urls])
		text = form.instance.content
		for url in urls:
			text = text.replace(url, "")
		
		form.instance.clean_content = text
		form.instance.links = urls

		form.save()
		return redirect('post-detail',slug=form.instance.slug)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False
	def get_context_data(self, **kwargs):
		active = {'ActiveHome':'active'}
		context = super().get_context_data(**kwargs)
		context['active'] = active
		return context



class APIDeletePost(APIView):
	authentication_classes = [authentication.SessionAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request,slug=None, format=None):
		slug = self.kwargs.get('slug')
		user = self.request.user
		post = get_object_or_404(Post,slug=slug)
		deleted = False
		comments = Comment.objects.filter(post=post)
		if user.is_authenticated:
			if user == post.author:
				for comment in comments:
					replies = Reply.objects.filter(comment=comment)
					for reply in replies:
						reply.delete()
					comment.delete()

				post.delete()
				deleted = True

		data = {"deleted":deleted} 
		return Response(data)






from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import ListView

from System.models import Profile

from urllib.parse import quote_plus

from django.db.models import Q

from django.contrib import messages

from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	UserPassesTestMixin
	)
from django.core import serializers
from Post.models import Post,RecommendPost
#def home(request):
	#return render(request,"home.html")
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import View,DetailView,ListView

from django.contrib.auth.models import User

from io import StringIO
import io
import re

from django.views.generic import RedirectView


from Post.models import Post,RecommendPost
from Comment.models import Comment,Reply

from django.utils import timezone


import json

from django.db.models import Count
class PostListRecommended(ListView):
	model         = Post
	template_name = "home.html"
	context_object_name = 'posts'
	post_list =  serializers.serialize("json", Post.objects.all())
	Recomendedpost_list =  serializers.serialize("json", RecommendPost.objects.all())

	parse_json = json.loads(post_list)
	parse_json2 = json.loads(post_list)

	i=0
	for item in parse_json:
		parse_json2[i]['functions'] = dict(comments_all='2')
		i+=1

	post_list = parse_json2

	NoramlPosts = False
	RecommendedPosts = True
	JusetUsers = False
	query = ''
	def get_queryset(self):
		queryset_list = RecommendPost.objects.filter(post__draft = False)[:5]
		query = self.request.GET.get('q')
		self.query = query
		
		if query:
			first_letter = query[0]
			if first_letter == '@':
				query2 = query.replace('@','',1)
				queryset_list = Profile.objects.filter(
				Q(user__username__icontains=query2)|
				Q(description__icontains=query2)|
				Q(slug__icontains=query2)|
				Q(user__first_name__icontains=query2)
				).distinct()[:6]


				self.context_object_name = 'profiles'
				self.NoramlPosts = False
				self.RecommendedPosts = False
				self.JusetUsers = True
			elif query == 'all_the_posts':
				queryset_list = Post.objects.filter(draft=False)[:5]

				self.NoramlPosts = True
				self.RecommendedPosts = False
				self.JusetUsers = False
			else:
				queryset_list_post = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count','-date_posted').filter(
					Q(author__username__icontains=query)|
					Q(content__icontains=query)|
					Q(slug__icontains=query)|
					Q(author__first_name__icontains=query),
					draft=False
					).distinct()[:5]

				if not queryset_list_post:
					queryset_list = Profile.objects.filter(
						Q(user__username__icontains=query)|
						Q(description__icontains=query)|
						Q(slug__icontains=query)|
						Q(user__first_name__icontains=query)
						).distinct()[:6]
					self.context_object_name = 'profiles'
					self.JusetUsers = True
				else:

					queryset_list = queryset_list_post

				self.NoramlPosts = True
				self.RecommendedPosts = False

		if not queryset_list:
			messages.error(self.request,f"Your search -{self.request.GET.get('q')}- did not match any documents.")

		return queryset_list
		

	def get_context_data(self, **kwargs):
		active = {'query':self.query,'post_list':self.post_list,'ActiveHome':'active','HomeBlock':'d-block','HomeBlockMd':'d-md-block','HomeNoneMd':'d-md-none'
		,'NoramlPosts':self.NoramlPosts,'RecommendedPosts':self.RecommendedPosts,'JusetUsers':self.JusetUsers,'Recomendedpost_list':self.Recomendedpost_list}
		context = super().get_context_data(**kwargs)
		context['active'] = active
		return context




class LoadMoreSearchedPosts(View):
	def get(self,request, *args, **kwargs):
		posts_loaded  = request.GET.get('posts_loaded')
		PL = int(posts_loaded)
		PLNew = PL - 5
		query = self.request.GET.get('query')

		if query != 'all_the_posts':
			post_list = serializers.serialize("json",Post.objects.annotate(like_count=Count('likes')).order_by('-like_count','-date_posted').filter(
				Q(author__username__icontains=query)|
				Q(content__icontains=query)|
				Q(slug__icontains=query)|
				Q(author__first_name__icontains=query),
				draft=False
				).distinct()[PLNew:PL])
		else:
			post_list = serializers.serialize("json",Post.objects.filter(draft=False)[PLNew:PL])
		

		json_data = json.loads(post_list)
		json_data2 = json.loads(post_list)

		for post in Post.objects.all():
			i=0
			for item in json_data:
				if post.id == item['pk']:
					liked = False
					follows_you = False
					post_for_you = False
					if request.user.is_authenticated:
						if request.user.profile in post.author.profile.following.all():
							follows_you = True
						if request.user.profile in post.likes.all():
							liked = True
						if request.user == post.author:
							post_for_you = True

					if post.draft:
						del json_data[i]
						del json_data2[i]
					else:
						json_data2[i]['functions'] = dict(comments_all=post.comments_all().count(),links_all=post.links_all())

						json_data2[i]['urls'] = dict(
							get_absolute_url_2 = post.get_absolute_url_2(),
							post_edit_url = post.post_edit_url(),
							post_delete_url = post.delete_post_api_url(),
							profile_url = post.author.profile.get_absolute_url(),
							add_like_url = post.add_like_url(),
							api_add_like_url = post.api_add_like_url(),
							)
						if post.image:
							image = post.image.url
						else:
							image = False

						content_list = post.clean_content
						content_list = list(content_list.split(" "))
						#Just content
						just_content = post.content
						just_content = re.sub("<", "&lt;", just_content)
						just_content = re.sub(">", "&gt;", just_content)

						#Just Name
						just_Name = post.author.first_name
						just_Name = re.sub("<", "&lt;",just_Name)
						just_Name = re.sub(">", "&gt;",just_Name)

						#Just_username
						just_username = post.author.username
						just_username = re.sub("<", "&lt;",just_username)
						just_username = re.sub(">", "&gt;",just_username)


						json_data2[i]['fields'] = dict(
							content = just_content,
							clean_content = post.clean_content,
							content_list = content_list,
							slug = post.slug,
							id = post.id,
							author = just_username,
							Name = just_Name,
							date_posted = post.date_posted,
							profile_image = post.author.profile.image.url,
							image = image,
							is_veryfied = post.author.profile.veryfied,
							likes = post.likes.count(),
							liked = liked,
							follows_you = follows_you,
							post_for_you = post_for_you,
							links = post.links,
							)
				i+=1
						
			post_list = json_data2

		data= {"posts":post_list}

		return JsonResponse(data,safe=False)


class LoadMoreProfiles(View):
	def get(self,request, *args, **kwargs):
		posts_loaded  = request.GET.get('posts_loaded')
		PL = int(posts_loaded)
		PLNew = PL - 6
		query = self.request.GET.get('query')

		profile_list = serializers.serialize("json",Profile.objects.filter(
				Q(user__username__icontains=query)|
				Q(description__icontains=query)|
				Q(slug__icontains=query)|
				Q(user__first_name__icontains=query)
			).distinct()[PLNew:PL])
		

		json_data = json.loads(profile_list)
		json_data2 = json.loads(profile_list)

		for profile in Profile.objects.all():
			i=0
			for item in json_data:
				if profile.id == item['pk']:
					follows_you = False
					you_are_the_user = False
					followed = False

					if request.user.is_authenticated:
						if request.user.profile in profile.following.all():
							follows_you = True
						if request.user == profile.user:
							you_are_the_user = True
						if profile in request.user.profile.following.all():
							followed = True


					json_data2[i]['urls'] = dict(
						get_absolute_url = profile.get_absolute_url(),
						follow_api_url = profile.api_follow_url()
							)

					#Just description
					just_description = profile.description
					just_description = re.sub("<", "&lt;", just_description)
					just_description = re.sub(">", "&gt;", just_description)

					#Just Name
					just_Name = profile.user.first_name
					just_Name = re.sub("<", "&lt;",just_Name)
					just_Name = re.sub(">", "&gt;",just_Name)

					#Just_username
					just_username = profile.user.username
					just_username = re.sub("<", "&lt;",just_username)
					just_username = re.sub(">", "&gt;",just_username)
					no_links = False

					if not profile.twitter and not profile.youtube and not profile.instagram and not profile.facebock:
						no_links = True

					followers = profile.followers.count()

					json_data2[i]['fields'] = dict(
							description = just_description,
							slug = profile.slug,
							id = profile.id,
							username = just_username,
							Name = just_Name,
							timestamp = 'profile.timestamp',
							profile_image = profile.image.url,
							background_image = profile.background_image.url,
							is_veryfied = profile.veryfied,
							follows_you = follows_you,
							you_are_the_user = you_are_the_user,
							twitter = profile.twitter,
							youtube = profile.youtube,
							instagram = profile.instagram,
							facebock = profile.facebock,
							no_links = no_links,
							followed = followed,
							followers = followers
							)
				i+=1
						
			post_list = json_data2

		data= {"posts":post_list}

		return JsonResponse(data,safe=False)


class FollowedPosts(LoginRequiredMixin,ListView):
	model         = Post
	template_name = "followed_posts_list.html"
	context_object_name = 'posts'
	
	post_list = Post.objects.filter(draft=False)
	def get(self, request, *args, **kwargs):
		user = User.objects.get(username=request.user.username)
		profile = Profile.objects.get(user=user)
		followings = profile.following.all()
		
		self.post_list = Post.objects.filter(draft=False,author__profile__in = followings)[:5]
		

		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		active = {'post_list':self.post_list,'ActiveFollowing':'active','HomeBlock':'d-block','HomeBlockMd':'d-md-block','HomeNoneMd':'d-md-none'}
		context = super().get_context_data(**kwargs)
		context['active'] = active
		return context
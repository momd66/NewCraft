from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

from django.utils.decorators import method_decorator


from .forms import (
	UserRegisterForm,
	UserLoginForm,
	ProfileUpdateForm,
	UserUpdateForm
	)


from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout

	)

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import View,DetailView,ListView

from django.contrib.auth.models import User
from .models import Profile

from io import StringIO
import io
from PIL import Image

from django.views.generic import RedirectView

from django.core.paginator import Paginator

from Post.models import Post,RecommendPost
from Comment.models import Comment,Reply

from django.utils import timezone

def RegisterView(request):
	next = request.GET.get("next")
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user      = form.save(commit=False)
		password1 = form.cleaned_data.get("password1")
		user.set_password(password1)
		username = form.cleaned_data.get("username")
		user.username = ("@"+username)
		user.save()

		return redirect("login")

	context ={
	"form":form,
	"ActiveRegister":"active"
	}

	return render(request, "register.html",context)



def LoginView(request):
	next = request.GET.get("next")
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		email    = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		user     = authenticate(email=email,password=password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect("/")

	context ={
	"form":form,
	"ActiveLogin":"active"
	}

	return render(request, "login.html",context)


@login_required
def profile(request):

	context={'ActiveProfile':'activeimg',"NoneProfile":"d-none",'userUsername':'momd',}

	return render(request,"profile.html",context)

		
@login_required
def UpdateProfile(request):
	if request.method == "POST":
		p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
		if p_form.is_valid():
			p_form.save()
			return redirect("profile")
	else:
		p_form = ProfileUpdateForm()

	context={'ActiveProfile':'active','p_form':p_form}
	return render(request,"update_profile.html",context)




class ProfileUpdate(View):
	def get(self,request):
		username = request.user.username
		name2 = request.GET.get('username2',None)
		description2 = request.GET.get('description2',None)
		twitter2 = request.GET.get('twitter2',None)
		instagram2 = request.GET.get('instagram2',None)
		youtube2 = request.GET.get('youtube2',None)
		facebock2 = request.GET.get('facebock2',None)


		if name2 != '':
			countName = len(name2)
			if countName >= 21:
				raise forms.ValidationError("The username max length is 20 letters!")
			else:
				obj = User.objects.get(username=username)
				obj.first_name = name2
				obj.save()

		else:
			raise forms.ValidationError("The name is Requeired")


		countDescription = len(description2)
		if countDescription > 250:
			raise forms.ValidationError("This descrption is to long!")
	

		obj2 = Profile.objects.get(user=obj)
		obj2.description = description2
		if obj2.twitter != twitter2:
			obj2.twitter = twitter2
		if obj2.instagram != instagram2:
			obj2.instagram = instagram2
		if obj2.youtube != youtube2:
			obj2.youtube = youtube2
		if obj2.facebock != facebock2:
			obj2.facebock = facebock2
		obj2.save()


		profile = {
		'username':obj.first_name,
		'description':obj2.description,
		'twitter':obj2.twitter,
		'instagram':obj2.instagram,
		'youtube':obj2.youtube,
		'facebock':obj2.facebock
		}

		data={'profile':profile}

		return JsonResponse(data)

import re

class AddComment(View):
	def get(self,request,slug, *args, **kwargs):
		user = request.user
		posts = Post.objects.filter(slug=slug).all()
		content  = request.GET.get('comment',None)
		commented = False

		countComment = len(content)

		too_long = countComment >= 256
			

		if user.is_authenticated:
			if content != '':
				if not too_long:
					obj = Comment.objects.create(
						user = user,content = content
						)
					for post in posts:
						obj.post.add(post)


					the_content = obj.content
					urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', the_content)

					text = obj.content

					content_link = re.sub("<.*?>", " ", obj.content)

					#Just content
					just_content = obj.content
					just_content = re.sub("<", "&lt;", just_content)
					just_content = re.sub(">", "&gt;", just_content)


					for url in urls:
						text = text.replace(url, "")
						link = url.replace(" ", "")


					obj.clean_content = text
					obj.links = urls
					obj.save()

					commented = True


		data={'commented':commented,'content':just_content,'slug':obj.slug}

		return JsonResponse(data)

class AddToRecommendition(View):
	def get(self,request,slug, *args, **kwargs):
		user = request.user
		post = Post.objects.get(slug=slug)
		recommended = False
	
		if user.is_authenticated:
			if user.is_superuser:
				if post.recommended:
					obj = RecommendPost.objects.filter(post = post).first()
					obj.delete()
					post.recommended = False
					post.save()
					recommended = False

				else:
					obj = RecommendPost.objects.create(
						post = post
						)
					post.recommended = True
					post.save()
					recommended = True
					
				
		data={'recommended':recommended}

		return JsonResponse(data)


class AddReply(View):
	def get(self,request,slug, *args, **kwargs):
		user = request.user
		posts = Comment.objects.filter(slug=slug).all()
		content  = request.GET.get('comment',None)
		commented = False

		countComment = len(content)
		too_long = countComment >= 256
			
		if user.is_authenticated:
			if content != '':
				if not too_long:
					obj = Reply.objects.create(
						user = user,
						content = content
						)
					for post in posts:
						obj.comment.add(post)

					

					the_content = obj.content
					urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', the_content)

					#Just content
					just_content = obj.content
					just_content = re.sub("<", "&lt;", just_content)
					just_content = re.sub(">", "&gt;", just_content)

					text = obj.content
					content_link = re.sub("<.*?>", " ", obj.content)
					sent_content = re.sub("<.*?>", " ", obj.content)
					for url in urls:
						text = text.replace(url, "")

					obj.clean_content = text
					obj.links = urls
					obj.save()

					commented = True

			

		data={'commented':commented,'content':just_content,'id':obj.id}

		return JsonResponse(data)

from Post.models import Post
	
class ProfileDetail(DetailView):
	model         = Profile
	template_name = "user_detail.html"
	
	active = {'ActiveHomeno':'active'}
	comments = ''

	def get(self, request,slug, *args, **kwargs):
		comments = Comment.objects.all()
		self.comments = comments
		profile = Profile.objects.filter(slug=slug).first()
		u = profile.user
		post_list = Post.objects.filter(author=u)[3:6]
		first_3_posts = Post.objects.filter(author=u)[:3]


		followers = profile.followers.all().order_by('user')[:3]
		followers_all = profile.followers.all().order_by('user')



		following = profile.following.all().order_by('user')[:3]
		following_all = profile.following.all().order_by('user')

		user_following = Following.objects.filter(user=u)[:3]

		user_following_10 = Following.objects.filter(user=u)[:10]

		user_following_all = Following.objects.filter(user=u)

		user_followers = Following.objects.filter(to_user=u)[:3]

		user_followers_10 = Following.objects.filter(to_user=u)[:10]

		user_followers_all = Following.objects.filter(to_user=u)
		following_more_10 = False
		if user_following_all.count() > 10:
			following_more_10 = True

		followers_more_10 = False
		if user_followers_all.count() > 10:
			followers_more_10 = True

		if request.user.is_authenticated:

			p2 = request.user.profile


	


			self.active = {
			'ActiveHomeno':'active',
			'u':u,
			'post_list':post_list,
			'post_list_3':first_3_posts,
			'comments':self.comments,
			'followers_list':user_followers,
			'followers_10':user_followers_10,
			'followers_all':user_followers_all,
			'following_list':user_following,
			'following_10':user_following_10,
			'following_all':user_following_all,
			'following_more_10':following_more_10,
			'followers_more_10':followers_more_10

			}

		else:
			self.active = {
			'ActiveHomeno':'active',
			'post_list':post_list,
			'post_list_3':first_3_posts,
			'followers_list':user_followers,
			'followers_10':user_followers_10,
			'followers_all':followers_all,
			'following_list':user_following,
			'following_10':user_following_10,
			'following_all':user_following_all,
			'following_more_10':following_more_10,
			'followers_more_10':followers_more_10
		}

		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['active'] = self.active
		return context


from django.core import serializers

class LoadMorePost(View):
	def get(self,request,slug, *args, **kwargs):
		posts_loaded  = request.GET.get('posts_loaded')
		PL = int(posts_loaded)
		PLNew = PL + 8
		profile = Profile.objects.get(slug=slug)
		if request.user == profile.user:
			post_list = Post.objects.filter(author=profile.user)[PL:PLNew]
		else:
			post_list = Post.objects.filter(author=profile.user,draft=False)[PL:PLNew]


		posts = serializers.serialize('json', list(post_list),
		 fields=('slug','content','draft','image','author','veryfied','date_posted'))
		data= {"posts":posts}

		return JsonResponse(data,safe=False)
import json
import datetime
from time import time, ctime
class LoadMorePostHome(View):
	def get(self,request, *args, **kwargs):
		last_id  = request.GET.get('last_id')
		id_ = int(last_id)
		post_list = serializers.serialize("json", RecommendPost.objects.filter(post__draft = False,id__lt=id_)[:5])

		json_data = json.loads(post_list)
		json_data2 = json.loads(post_list)


		for post in Post.objects.all():
			i=0
			for item in json_data:
				if post.id == item['fields']['post']:
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

class LoadMorePostFollwings(View):
	def get(self,request, *args, **kwargs):
		last_id  = request.GET.get('last_id')
		id_ = int(last_id)
		the_user = User.objects.get(username=request.user.username)
		the_profile = Profile.objects.get(user=the_user)
		the_followings = the_profile.following.all()
		post_list = serializers.serialize("json", Post.objects.filter(draft = False,author__profile__in = the_followings,id__lt=id_)[:5])

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



class LoadMoreUserPosts(View):
	def get(self,request,slug, *args, **kwargs):
		last_id  = request.GET.get('last_id')
		id_ = int(last_id)
		profile = Profile.objects.get(slug=slug)
		if request.user == profile.user:
			post_list = serializers.serialize("json", Post.objects.filter(author=profile.user,id__lt=id_)[:5])
		else:
			post_list = serializers.serialize("json", Post.objects.filter(draft=False,author=profile.user,id__lt=id_)[:5])
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
						draft=post.draft
						)
				i+=1
						
			post_list = json_data2

		data= {"posts":post_list}

		return JsonResponse(data,safe=False)

from django.db.models import Count
from django.db.models import Case, When

class LoadMoreComments(View):
	def get(self,request,slug, *args, **kwargs):
		posts_loaded  = request.GET.get('posts_loaded')
		PL = int(posts_loaded)
		PLNew = PL - 5
		post = Post.objects.get(slug=slug)
		#post_list = serializers.serialize("json", Comment.objects.filter(post=post).order_by('-timestamp')[PLNew:PL])
		ids_at_top = [request.user.id]
		post_list = serializers.serialize("json", Comment.objects.annotate(like_count=Count('likes')).order_by(Case(When(user__id__in=ids_at_top, then=0), default=1),'-like_count','-timestamp').filter(post=post)[PLNew:PL])
		
		json_data = json.loads(post_list)
		json_data2 = json.loads(post_list)

		for post in Comment.objects.all().order_by('-timestamp'):
			i=0
			for item in json_data:
				if post.id == item['pk']:
					liked = False
					post_for_you = False
					if request.user.is_authenticated:
						if request.user.profile in post.likes.all():
							liked = True
						if request.user == post.user:
							post_for_you = True

					json_data2[i]['functions'] = dict(replies_count=post.replies_all().count(),links_all=post.links_all())

					json_data2[i]['urls'] = dict(
						get_absolute_url = post.get_absolute_url(),
						post_delete_api_url = post.comment_delete_api_url(),
						profile_url = post.user.profile.get_absolute_url(),
						add_like_url = post.add_like_comment_url(),
						api_add_like_url = post.add_like_comment_api_url(),
						)



					content_list = post.clean_content
					content_list = list(content_list.split(" "))
					if post.replies_all():
						replies = True
					else:
						replies = False

					if post.replies_all().count() > 2:
						replies_gt_2 = True
					else:
						replies_gt_2 = False

					#Just content
					just_content = post.content
					just_content = re.sub("<", "&lt;", just_content)
					just_content = re.sub(">", "&gt;", just_content)

					#Just Name
					just_Name = post.user.first_name
					just_Name = re.sub("<", "&lt;",just_Name)
					just_Name = re.sub(">", "&gt;",just_Name)

					#Just_username
					just_username = post.user.username
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
						date_posted = post.timestamp,
						profile_image = post.user.profile.image.url,
						is_veryfied = post.user.profile.veryfied,
						likes = post.likes.count(),
						liked = liked,
						post_for_you = post_for_you,
						links = post.links,
						replies = replies,
						replies_gt_2 = replies_gt_2,
						replies_count = post.replies_all().count()
						)

					reply_list = serializers.serialize("json", post.replies())
					json_data_reply = json.loads(reply_list)
					json_data_reply2 = json.loads(reply_list)

					for postt in Reply.objects.all():
						ii=0
						for itemm in json_data_reply:
							if postt.id == itemm['pk']:
								liked = False
								post_for_you = False
								if request.user.is_authenticated:
									if request.user.profile in postt.likes.all():
										liked = True
									if request.user == postt.user:
										post_for_you = True

								json_data_reply2[ii]['functions'] = dict(links_all=postt.links_all())

								json_data_reply2[ii]['urls'] = dict(
									post_delete_api_url = postt.reply_delete_api_url(),
									profile_url = postt.user.profile.get_absolute_url(),
									api_add_like_url = postt.add_like_reply_api_url(),
									)

								#Just content
								r_just_content = postt.content
								r_just_content = re.sub("<", "&lt;", r_just_content)
								r_just_content = re.sub(">", "&gt;", r_just_content)

								#Just Name
								r_just_Name = postt.user.first_name
								r_just_Name = re.sub("<", "&lt;",r_just_Name)
								r_just_Name = re.sub(">", "&gt;",r_just_Name)

								#Just_username
								r_just_username = postt.user.username
								r_just_username = re.sub("<", "&lt;",r_just_username)
								r_just_username = re.sub(">", "&gt;",r_just_username)			

								json_data_reply2[ii]['fields'] = dict(
									content = r_just_content,
									clean_content = postt.clean_content,
									id = postt.id,
									author = r_just_username,
									Name = r_just_Name,
									date_posted = postt.timestamp,
									profile_image = postt.user.profile.image.url,
									is_veryfied = postt.user.profile.veryfied,
									likes = postt.likes.count(),
									liked = liked,
									post_for_you = post_for_you,
									links = postt.links
								)
							ii+=1
						json_data2[i]['replies'] = json_data_reply2

						 
				i+=1
						
			post_list = json_data2

		data= {"posts":post_list}

		return JsonResponse(data,safe=False)


class LoadMoreReplies(View):
	def get(self,request,slug, *args, **kwargs):
		posts_loaded  = request.GET.get('posts_loaded')
		PL = int(posts_loaded)
		PLNew = PL - 5
		post = Comment.objects.get(slug=slug)
		post_list = serializers.serialize("json", Reply.objects.filter(comment=post).order_by('timestamp')[PLNew:PL])
		json_data = json.loads(post_list)
		json_data2 = json.loads(post_list)

		for post in Reply.objects.all().order_by('-timestamp'):
			i=0
			for item in json_data:
				if post.id == item['pk']:
					liked = False
					post_for_you = False
					if request.user.is_authenticated:
						if request.user.profile in post.likes.all():
							liked = True
						if request.user == post.user:
							post_for_you = True



					json_data2[i]['functions'] = dict(links_all=post.links_all())

					json_data2[i]['urls'] = dict(
						post_delete_api_url = post.reply_delete_api_url(),
						profile_url = post.user.profile.get_absolute_url(),
						api_add_like_url = post.add_like_reply_api_url(),
						)

					#Just content
					just_content = post.content
					just_content = re.sub("<", "&lt;", just_content)
					just_content = re.sub(">", "&gt;", just_content)

					#Just Name
					just_Name = post.user.first_name
					just_Name = re.sub("<", "&lt;",just_Name)
					just_Name = re.sub(">", "&gt;",just_Name)

					#Just_username
					just_username = post.user.username
					just_username = re.sub("<", "&lt;",just_username)
					just_username = re.sub(">", "&gt;",just_username)

					json_data2[i]['fields'] = dict(
						content = just_content,
						clean_content = post.clean_content,
						id = post.id,
						author = just_username,
						Name = just_Name,
						date_posted = post.timestamp,
						profile_image = post.user.profile.image.url,
						is_veryfied = post.user.profile.veryfied,
						likes = post.likes.count(),
						liked = liked,
						post_for_you = post_for_you,
						links = post.links,
						)

						 
				i+=1
						
			post_list = json_data2

		data= {"posts":post_list}

		return JsonResponse(data,safe=False)






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
import os


from .models import Following

class APIFollow(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,slug=None, format=None):
    	slug = self.kwargs.get('slug')
    	profile = get_object_or_404(Profile,slug=slug)
    	user = self.request.user
    	to_user = profile.user
    	followed = False
    	if user.is_authenticated:
    		if not to_user == user:
    			if user.profile in to_user.profile.followers.all():
    				to_user.profile.followers.remove(user.profile)
    				user.profile.following.remove(to_user.profile)
    				following = Following.objects.filter(user = self.request.user,to_user = profile.user).first()
    				following.delete()
    			else:
    				to_user.profile.followers.add(user.profile)
    				user.profile.following.add(to_user.profile)
    				follow = Following.objects.get_or_create(
    						user = user,
    						to_user = to_user
    						)
    				followed = True



    	data = {"followed":followed} 

    	return Response(data)



		








class AddLike(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		post = get_object_or_404(Post,slug=slug)
		user = self.request.user
		url_ = user.profile.get_absolute_url()
		post_user = post.author
		if user.is_authenticated:
			if user.profile in post.likes.all():
				post.likes.remove(user.profile)
			else:
				post.likes.add(user.profile)
		return url_

class APIAddLike(APIView):
	authentication_classes = [authentication.SessionAuthentication]
	permission_classes = [permissions.IsAuthenticated]


	def get(self, request,slug=None, format=None):
		slug = self.kwargs.get('slug')
		post = get_object_or_404(Post,slug=slug)
		user = self.request.user
		post_user = post.author
		
		if user.is_authenticated:
			if user.profile in post.likes.all():
				post.likes.remove(user.profile)
				like = False
			else:
				post.likes.add(user.profile)
				like = True


		data = {"like":like} 
		return Response(data)



class AddLikeComment(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		comment = get_object_or_404(Comment,slug=slug)
		user = self.request.user
		url_ = user.profile.get_absolute_url()
		comment_user = comment.user
		if user.is_authenticated:
			if user.profile in comment.likes.all():
				comment.likes.remove(user.profile)
			else:
				comment.likes.add(user.profile)
		return url_

class APIAddLikeComment(APIView):
	authentication_classes = [authentication.SessionAuthentication]
	permission_classes = [permissions.IsAuthenticated]


	def get(self, request,slug=None, format=None):
		slug = self.kwargs.get('slug')
		comment = get_object_or_404(Comment,slug=slug)
		user = self.request.user
		url_ = user.profile.get_absolute_url()
		comment_user = comment.user
		if user.is_authenticated:
			if user.profile in comment.likes.all():
				comment.likes.remove(user.profile)
				like = False
			else:
				comment.likes.add(user.profile)
				like = True


		data = {"like":like} 
		return Response(data)

class APIAddLikeReply(APIView):
	authentication_classes = [authentication.SessionAuthentication]
	permission_classes = [permissions.IsAuthenticated]


	def get(self, request,id=None, format=None):
		slug = self.kwargs.get('slug')
		comment = get_object_or_404(Reply,id=id)
		user = self.request.user
		comment_user = comment.user
		if user.is_authenticated:
			if user.profile in comment.likes.all():
				comment.likes.remove(user.profile)
				like = False
			else:
				comment.likes.add(user.profile)
				like = True


		data = {"like":like} 
		return Response(data)




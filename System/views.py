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
from .models import Profile,FriendRequest

from io import StringIO
import io
from PIL import Image

from django.views.generic import RedirectView

from django.core.paginator import Paginator

def RegisterView(request):
	next = request.GET.get("next")
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user      = form.save(commit=False)
		password1 = form.cleaned_data.get("password1")
		user.set_password(password1)
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
#	p = Profile.objects.filter(slug=slug).first()
#	u = p.user
#	sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
#	rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)

#	friends = p.friends.all()

	#is this user our friend
#	button_status = 'none'
#	if p not in request.user.profile.friends.all():
#		button_status = 'not_friend'


		#if we have sent him a friend request
#		if len(FriendRequest.objects.filter(from_user=request.user).filter(to_user=p.user)) == 1:
#			button_status = 'friend_request_sent'



	context={
	'ActiveProfile':'activeimg',
	"NoneProfile":"d-none",
	'userUsername':'momd',
#	'u':u,
#	'button_status':button_status,
#	'friends_list':friends,
#	'sent_friend_requests':sent_friend_requests,
#	'rec_friend_requests':rec_friend_requests
	}

	return render(request,"profile.html",context)

		

@login_required
def UpdateProfile(request):
	if request.method == "POST":
		p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
		if p_form.is_valid():
			p_form.save()
			#messages.success(request,f"Your Account has been updated!")
			return redirect("profile")
	else:
		p_form = ProfileUpdateForm()

	context={'ActiveProfile':'active','p_form':p_form}
	return render(request,"update_profile.html",context)


class ProfileUpdate(View):
	def get(self,request):
		username = request.user.username
		username2 = request.GET.get('username2',None)
		description2 = request.GET.get('description2',None)

		countUsername = len(username2)
		if countUsername >= 21:
			raise forms.ValidationError("The username max length is 20 letters!")
		if ' ' in username2:
			raise forms.ValidationError("You can't use space in usernames")
		if not description2:
			raise forms.ValidationError("description requerired")

		obj = User.objects.get(username=username)
		obj.username = username2
		obj.save()

		countDescription = len(description2)
		if countDescription > 250:
			raise forms.ValidationError("This descrption is to long!")

			

		obj2 = Profile.objects.get(user=obj)
		obj2.description = description2
		obj2.save()


		profile = {'username':obj.username,'description':obj2.description}

		data={'profile':profile}

		return JsonResponse(data)


class ProfileDetail(DetailView):
	model         = Profile
	template_name = "user_detail.html"
	#active = {'ActiveHome':'active'}
	active = {
			'ActiveHome':'active'
		}

	def get(self, request,slug, *args, **kwargs):
		p = Profile.objects.filter(slug=slug).first()
		u = p.user
		friendsFull = p.friends.all().order_by('user')

		paginator1 = Paginator(friendsFull, 3)

		page_number = request.GET.get('page')

		friends = paginator1.get_page(page_number)

		if request.user.is_authenticated:
			#slug = request.user.profile.slug
			#user = request.user
			sent_friend_requestsFull = FriendRequest.objects.filter(from_user=p.user)
			paginator2 = Paginator(sent_friend_requestsFull, 3)

			sent_friend_requests = paginator2.get_page(page_number)

			rec_friend_requestsFull = FriendRequest.objects.filter(to_user=p.user)
			paginator3 = Paginator(rec_friend_requestsFull, 3)

			rec_friend_requests = paginator3.get_page(page_number)
			
			p2 = request.user.profile

			#is this user our friend
			button_status = 'none'
			if p not in request.user.profile.friends.all():
				button_status = 'not_friend'

				#if we have sent him a friend request
				if len(FriendRequest.objects.filter(
					from_user=request.user).filter(to_user=p.user)) == 1:
						button_status = 'friend_request_sent'

				elif len(FriendRequest.objects.filter(
					from_user=p.user).filter(to_user=request.user)) == 1:
						button_status = 'rec_request'

			else:
				button_status = 'friends'
	


			self.active = {
			'ActiveHome':'active',
			'u':u,
			'button_status':button_status,
			'friends_list':friends,"full_friends_list":friendsFull,
			'full_rec_friend_requests':rec_friend_requestsFull,
			'sent_friend_requests':sent_friend_requests,
			'rec_friend_requests':rec_friend_requests,
			'full_sent_friend_requests':sent_friend_requestsFull
			}

		else:
			self.active = {
			'ActiveHome':'active',
			'friends_list':friends,
			"full_friends_list":friendsFull
		}

		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['active'] = self.active
		return context






class SendFriendRequestOLD(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		profile = get_object_or_404(Profile,slug=slug)
		url_ = profile.get_absolute_url()
		user = self.request.user
		to_user = profile.user
		if user.is_authenticated:
			if not to_user == user:
				request, created = FriendRequest.objects.get_or_create(
					from_user = user,
					to_user = to_user
					)
				to_user.profile.from_user.add(user.profile)
				user.profile.to_user.add(to_user.profile)

		return url_

class SendFriendRequest(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		profile = get_object_or_404(Profile,slug=slug)
		url_ = profile.get_absolute_url()
		user = self.request.user
		to_user = profile.user

		if user.is_authenticated:
			if not to_user == user:
				if not FriendRequest.objects.filter(from_user = to_user,to_user = user):
					if not to_user.profile in user.profile.friends.all():
						if not FriendRequest.objects.filter(from_user = user,to_user = to_user):
							request, created = FriendRequest.objects.get_or_create(
								from_user = user,
								to_user = to_user
								)
							to_user.profile.from_user.add(user.profile)
							user.profile.to_user.add(to_user.profile)
		return url_



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
import os
class APISendFriendRequest(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,slug=None, format=None):
    	slug = self.kwargs.get('slug')
    	profile = get_object_or_404(Profile,slug=slug)
    	url_ = profile.get_absolute_url()
    	user = self.request.user
    	to_user = profile.user
    	sent = False
    	canceled = False
    	rec_request = False
    	friends = False
    	ignored = False
    	if user.is_authenticated:
    		if not to_user == request.user:
    			if FriendRequest.objects.filter(from_user = to_user,to_user = user):
    				rec_request = True
    			elif to_user.profile in user.profile.friends.all() :
    				friends = True
    			else:
    				if not FriendRequest.objects.filter(from_user = user,to_user = to_user):
    					request, created = FriendRequest.objects.get_or_create(
    						from_user = user,
    						to_user = to_user
    						)
    					to_user.profile.from_user.add(user.profile)
    					user.profile.to_user.add(to_user.profile)
    					sent = True
    				else:
    					frequest = FriendRequest.objects.filter(from_user = user,to_user = to_user).first()
    					if frequest:
    						frequest.delete()
    						to_user.profile.from_user.remove(user.profile)
    						user.profile.to_user.remove(to_user.profile)
    						canceled = True


    	data = {"sent":sent,"canceled":canceled,"rec_request":rec_request,"friends":friends} 

    	return Response(data)




class CancelFriendRequest(RedirectView):
	def get_redirect_url(self, *args, **kwargs):			
		slug = self.kwargs.get('slug')
		profile = get_object_or_404(Profile,slug=slug)
		url_ = profile.get_absolute_url()
		if self.request.user.is_authenticated:
			frequest = FriendRequest.objects.filter(from_user = self.request.user,to_user = profile.user).first()
			if frequest:
				frequest.delete()
				profile.from_user.remove(self.request.user.profile)
				self.request.user.profile.to_user.remove(profile)
		return url_
		
class APICancelFriendRequest(APIView):
	authentication_classes = [authentication.SessionAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request,slug=None, format=None):	
		slug = self.kwargs.get('slug')
		profile = get_object_or_404(Profile,slug=slug)
		url_ = profile.get_absolute_url()
		canceled = False
		if self.request.user.is_authenticated:
			if not to_user == request.user:
				if FriendRequest.objects.filter(from_user = self.request.user,to_user = profile.user):
					frequest = FriendRequest.objects.filter(from_user = self.request.user,to_user = profile.user).first()
					if frequest:
						frequest.delete()
						profile.from_user.remove(self.request.user.profile)
						self.request.user.profile.to_user.remove(profile)
						canceled = True


		data = {"canceled":canceled} 
		return Response(data)




class AcceptFriendRequest(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		profile = get_object_or_404(Profile,slug=slug)
		user = self.request.user
		url_ = user.profile.get_absolute_url()
		from_user = profile.user
		frequest = FriendRequest.objects.filter(from_user=from_user,to_user=user).first()
		if user.is_authenticated:
			if not user == from_user:
				if frequest:
					user1 = frequest.to_user
					user2 = from_user
					user1.profile.friends.add(user2.profile)
					user2.profile.friends.add(user1.profile)
					frequest.delete()
					user1.profile.from_user.remove(user2.profile)
					user2.profile.to_user.remove(user1.profile)
		return url_

class APIAcceptFriendRequest(APIView):
	authentication_classes = [authentication.SessionAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request,slug=None, format=None):
		slug = self.kwargs.get('slug')
		profile = get_object_or_404(Profile,slug=slug)
		user = self.request.user
		from_user = profile.user
		accepted = False
		frequest = FriendRequest.objects.filter(from_user=from_user,to_user=user).first()
		if user.is_authenticated:
			if not user == from_user:
				if frequest:
					user1 = frequest.to_user
					user2 = from_user
					user1.profile.friends.add(user2.profile)
					user2.profile.friends.add(user1.profile)
					frequest.delete()
					user1.profile.from_user.remove(user2.profile)
					user2.profile.to_user.remove(user1.profile)
					accepted = True


		data = {"accepted":accepted} 
		return Response(data)



class DeleteFriendRequest(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs.get('slug')
		profile = get_object_or_404(Profile,slug=slug)
		user = self.request.user
		url_ = user.profile.get_absolute_url()
		from_user = profile.user
		frequest = FriendRequest.objects.filter(from_user=from_user,to_user=user).first()
		if user.is_authenticated:
			if not user == from_user:
				if frequest:
					frequest.delete()
					from_user.profile.to_user.remove(user.profile)
					user.profile.from_user.remove(from_user.profile)
		return url_

class APIDeleteFriendRequest(APIView):
	authentication_classes = [authentication.SessionAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request,slug=None, format=None):
		slug = self.kwargs.get('slug')
		profile = get_object_or_404(Profile,slug=slug)
		user = self.request.user
		from_user = profile.user
		ignored = False
		frequest = FriendRequest.objects.filter(from_user=from_user,to_user=user).first()
		if user.is_authenticated:
			if not user == from_user:
				if frequest:
					frequest.delete()
					from_user.profile.to_user.remove(user.profile)
					user.profile.from_user.remove(from_user.profile)
					ignored = True


		data = {"ignored":ignored} 
		return Response(data)



class DeleteFriend(RedirectView):
	def get_redirect_url(self, *args, **kwargs):			
		slug = self.kwargs.get('slug')
		profile1 = self.request.user.profile
		profile2 = get_object_or_404(Profile,slug=slug)
		url_ = profile2.get_absolute_url()
		if self.request.user.is_authenticated:
			profile1.friends.remove(profile2)
			profile2.friends.remove(profile1)

		return url_
		
class APIDeleteFriend(APIView):
	authentication_classes = [authentication.SessionAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request,slug=None, format=None):
		slug = self.kwargs.get('slug')
		profile1 = self.request.user.profile
		profile2 = get_object_or_404(Profile,slug=slug)
		url_ = profile2.get_absolute_url()
		deleted = False
		if self.request.user.is_authenticated:
			profile1.friends.remove(profile2)
			profile2.friends.remove(profile1)
			deleted = True

		data = {"deleted":deleted} 
		return Response(data)
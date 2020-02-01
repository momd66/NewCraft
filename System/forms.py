from django import forms


from django.contrib.auth import (
	authenticate,
	get_user_model
	)

from .models import Profile

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
	username  = forms.CharField(widget=forms.TextInput(attrs={'maxlength':20}))
	email     = forms.EmailField(label="Email")
	password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
	password2 = forms.CharField(label="Confirm password",widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ["username","email","password1","password2"]


	def clean(self,*args,**kwargs):
		userName = self.cleaned_data.get("username")
		countUsername = len(userName)
		if countUsername >= 21:
			raise forms.ValidationError("The username max length is 20 letters!") 

		email    = self.cleaned_data.get("email") 

		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email is already being used")

		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 != password2:
			raise forms.ValidationError("Passwords must match!")

		return super(UserRegisterForm, self).clean(*args,**kwargs)




class UserLoginForm(forms.Form):
	email    = forms.CharField(widget=forms.EmailInput)
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self,*args,**kwargs):
		email    = self.cleaned_data.get("email")
		password = self.cleaned_data.get("password")

		if email and password:
			user = authenticate(email=email,password=password)

			if not user:
				raise forms.ValidationError("This user does not exist")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")

			if not user.is_active:
				raise forms.ValidationError("This user is not active")

		return super(UserLoginForm, self).clean(*args,**kwargs)





class UserUpdateForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'maxlength':20}))
	class Meta:
		model = User
		fields = ["username"]
	def clean_username(self, *args ,**kwargs):
		userName = self.cleaned_data.get("username")
		countUsername = len(userName)
		if countUsername >= 21:
			raise forms.ValidationError("Max length is 20 letters!") 
		else:
			return userName
			


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ["image","background_image"]
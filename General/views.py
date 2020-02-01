from django.shortcuts import render




from django.views.generic import ListView

from System.models import Profile

from urllib.parse import quote_plus

from django.db.models import Q

from django.contrib import messages


#def home(request):
	#return render(request,"home.html")


class Home(ListView):
	model         = Profile
	template_name = "home.html"
	context_object_name = 'profiles'
	#paginate_by = 3
	
	def get_queryset(self):
		queryset_list = Profile.objects.all()
		query = self.request.GET.get('q')
		

		if query:
			queryset_list = Profile.objects.filter(
				Q(user__username__icontains=query)|
				Q(description__icontains=query)|
				Q(slug__icontains=query)
				).distinct()

		if not queryset_list:
			messages.error(self.request,f"Your search -{self.request.GET.get('q')}- did not match any documents.")

			
		return queryset_list

	def get_context_data(self, **kwargs):
		active = {'ActiveHome':'active','HomeBlock':'d-block','HomeBlockMd':'d-md-block','HomeNoneMd':'d-md-none'}
		context = super().get_context_data(**kwargs)
		context['active'] = active
		return context



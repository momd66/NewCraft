from django.db import models


from Post.models import Post

from System.models import Profile

from django.conf import settings

from django.db.models.signals import pre_save

from django.utils.text import slugify


import random

from django.shortcuts import reverse

import operator


class Comment(models.Model):
	post    = models.ManyToManyField(Post,related_name='post')
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	content = models.TextField(max_length='255',null=False,blank=False)
	clean_content = models.TextField(max_length='255',null=True,blank=True)
	links       = models.TextField(max_length=255,null=True,blank=True)
	timestamp = models.DateTimeField(auto_now=True,auto_now_add=False)
	slug        = models.SlugField(unique=True)
	likes       = models.ManyToManyField(Profile,blank=True,related_name='likes2')
	

	def replies(self):
		reply_list = Reply.objects.filter(comment=self)[:2]
		return reply_list

	def replies_all(self):
		reply_list = Reply.objects.filter(comment=self)
		return reply_list

	def links_all(self):
		if self.links:
			links = self.links
			links2 = links.replace('[', "")
			links3 = links2.replace(']', "")
			links4 = links3.replace("'", "")
			links_list = list(links4.split(",")) 
			return links_list

	def __str__(self):
		return self.content

	def get_absolute_url(self):
		return reverse("comment-detail",kwargs={'slug':self.slug})
		
	def add_like_comment_url(self):
		return reverse("add-like-comment",kwargs={'slug':self.slug})

	def add_like_comment_api_url(self):
		return reverse("add-like-comment-api",kwargs={'slug':self.slug})

	def add_reply_url(self):
		return reverse("add-reply",kwargs={'slug':self.slug})

	def delete_comment(self):
		return reverse("comment-delete",kwargs={'slug':self.slug})

	def comment_delete_api_url(self):
		return reverse("comment-delete-api",kwargs={'slug':self.slug})

	def load_more_replies_url(self):
		return reverse("load-more-replies-comment",kwargs={'slug':self.slug})




class Reply(models.Model):
	comment = models.ManyToManyField(Comment,related_name='comment')
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	content = models.TextField(null=False,blank=False)
	clean_content = models.TextField(max_length='255',null=True,blank=True)
	links       = models.TextField(max_length=255,null=True,blank=True)
	timestamp = models.DateTimeField(auto_now=True,auto_now_add=False)
	likes       = models.ManyToManyField(Profile,blank=True,related_name='likes3')

	def add_like_reply_api_url(self):
		return reverse("add-like-reply-api",kwargs={'id':self.id})

	def reply_delete_api_url(self):
		return reverse("reply-delete-api",kwargs={'id':self.id})

	def __str__(self):
		return self.content	

	def links_all(self):
		if self.links:
			links = self.links
			links2 = links.replace('[', "")
			links3 = links2.replace(']', "")
			links4 = links3.replace("'", "")
			links_list = list(links4.split(",")) 
			return links_list






def create_slug(instance,new_slug=None):
	abc1 = '09654255435644233553354431245633453235'

	rabc1 = random.choice(abc1)

	abc2 = 'ABdBCDAUVyADSJSSGGSFXAITDPSSGCSqGDSwYBSQIXS'

	rabc2 = random.choice(abc2)

	abc3 = 'AbBcDauV09aSJsSGgsasa6xsSG6Cs8gDs2YBs0ixS'

	rabc3 = random.choice(abc3)

	abc4 = 'AB549BCDAUV9A0S7JS63S586GGS7F7XCS8G1DS2YBS0IXS'

	rabc4 = random.choice(abc4)

	abc5 = 'AbBcDauV9aSJsSGgsSfx2It8psSGCs8gDsZzv2YBs0ixS'

	rabc5 = random.choice(abc5)

	abc6 = 'AbBcDauxV9aSJsS9gSfx20It8pAddsSGCs8gDs2YBs0ixS'

	rabc6 = random.choice(abc6)

	abc7 = 'AbBcDaufdfdjkxV9aSJ327sS9gSfx20It8p690AddsSGCskj38gDs2YBs0ixS'

	rabc7 = random.choice(abc7)

	abc8 = 'AbBcDauxV9aSJsS9gSfx20It8pAdfhdjldsdffdsSGCs8gDs2YBs0ixS'

	rabc8 = random.choice(abc8)



	ran = (rabc1+rabc2+rabc3+rabc4+rabc5+rabc6+rabc7+rabc8)

	abcExtra = 'AsDSDSdhiSUDSjdoIdhsiaoudsiuhuyfhsiuhfiufgushfsoshaoishfuoigus'

	ranEX = random.choice(abcExtra)


	slug     =  slugify(ran)
	if new_slug is not None:
		slug = new_slug

	qs       = Comment.objects.filter(slug=slug).order_by('-id')
	exists   = qs.exists()
	

	
	if exists:
		new_slug = '%s-%s' %(slug,ranEX)
		return create_slug(instance,new_slug=new_slug)
	return slug



def pre_save_post_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)




pre_save.connect(pre_save_post_receiver,sender=Comment)



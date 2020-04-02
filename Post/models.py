from django.db import models

from django.contrib.auth.models import User

from PIL import Image

from django.utils import timezone

from django.shortcuts import reverse

from django.db.models.signals import pre_save

from django.utils.text import slugify

from System.models import Profile

import json
import re


import random

import io
from django.core.files.storage import default_storage as storage

class Post(models.Model):
	content     = models.TextField(max_length='500',null=False,blank=False)
	clean_content = models.TextField(max_length='500',null=True,blank=True)
	links       = models.TextField(max_length=500,null=True,blank=True)
	date_posted = models.DateTimeField(default=timezone.now)
	author      = models.ForeignKey(User,on_delete=models.CASCADE)
	image       = models.ImageField(upload_to='thubmnails',null=True,blank=True)
	draft       = models.BooleanField(default=False)
	slug        = models.SlugField(unique=True)
	likes       = models.ManyToManyField(Profile,blank=True,related_name='likes')
	edited      = models.BooleanField(default=False)
	recommended = models.BooleanField(default=False)
	



	publish_choose       = (
		('Public','Public'),
		('Private','Private')
		)
	privacy      = models.CharField(max_length=100,choices=publish_choose,default="Public")
	TimeChange   = models.IntegerField(default=0) 

	def comments_all(self):
		from Comment.models import Comment
		comment_list = Comment.objects.filter(post=self)
		return comment_list


	def links_all(self):
		if self.links:
			links = self.links
			links2 = links.replace('[', "")
			links3 = links2.replace(']', "")
			links4 = links3.replace("'", "")
			links_list = list(links4.split(",")) 
			return links_list

	def content_link(self):
		the_content = self.full_content
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', the_content)
		
		listToStr = ' '.join([str(elem) for elem in urls])

		text = ''
		for url in urls:
			text = the_content.replace(url, "<b>"+url+"</b>")


		return(text)

	def __str__(self):
		return self.author.username


	def get_absolute_url_2(self):
		return reverse("post-detail",kwargs={'slug':self.slug})

	def post_edit_url(self):
		return reverse("post-update",kwargs={'slug':self.slug})

	def post_delete_url(self):
		return reverse("post-delete",kwargs={'slug':self.slug})

	def add_like_url(self):
		return reverse("add-like",kwargs={'slug':self.slug})

	def api_add_like_url(self):
		return reverse("add-like-api",kwargs={'slug':self.slug})


	def add_comment_url(self):
		return reverse("add-comment",kwargs={'slug':self.slug})

	def delete_post_api_url(self):
		return reverse("post-delete-api",kwargs={'slug':self.slug})

	def recommend_url(self):
		return reverse("recommend",kwargs={'slug':self.slug})
		

	def load_more_comments_url(self):
		return reverse("load-more-comments-post",kwargs={'slug':self.slug})


	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if self.image:
			img_read = storage.open(self.image.name, 'r')
			img = Image.open(img_read)

			if img.height > 700 or img.width > 700:
				output_size = (700, 700)
				img.thumbnail(output_size)
				in_mem_file = io.BytesIO()

				try:
					img.save(in_mem_file, format='JPEG')
				except:
					img.save(in_mem_file, format='PNG')

				img_write = storage.open(self.image.name, 'w+')
				img_write.write(in_mem_file.getvalue())
				img_write.close()

			img_read.close()


	class Meta:
		ordering = ['-date_posted']



class RecommendPost(models.Model):
	post = models.OneToOneField(Post,on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now=True,auto_now_add=False)

	class Meta:
		ordering = ["-timestamp"]


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

	abc9 = 'AbBcDaurererexVadasx2dsddsdsrererdasda23332323ddd8pAddrererersSGCs8gD13Ds2YBs0ixS'

	rabc9 = random.choice(abc9)

	abc10 = 'AbBcDauxV9aSJsS9gSfx20It8pAddsSGCs8gDs2YBs0ixS'

	rabc10 = random.choice(abc10)

	abc11 = 'AbBcDauxVdasdadddsdsdsdsfx20It8pAddsSGCs8gDdsddsds55462213Ds2YBs0ixS'

	rabc11 = random.choice(abc11)

	abc12 = 'AbBcDauxVdsddsdsdsg9aSJsS9gSfx2gggf0It8pAgjhjhjgDs2YBs0ixS'

	rabc12 = random.choice(abc12)

	abc13 = 'AbBcDauxVdasdadddsdsdsdsfx20It8pAddsSGCs8gDdsddsds55462213Ds2YBs0ixS'

	rabc13 = random.choice(abc13)

	abc14 = 'AbBcDaurererexVadasx2dsddsdsrererdasda233323rsSGCs8gD13Ds2YBs0ixS'

	rabc14 = random.choice(abc14)



	ran = (rabc1+rabc2+rabc3+rabc4+rabc5+rabc6+rabc7+rabc8+rabc9+rabc10+rabc11+rabc12+rabc13+rabc14)

	abcExtra = 'AsDSDSdhiSUDSjdoIdhsiaoudsiuhuyfhsiuhfiufgushfsoshaoishfuoigus'

	ranEX = random.choice(abcExtra)


	slug     =  slugify(ran)
	if new_slug is not None:
		slug = new_slug

	qs       = Post.objects.filter(slug=slug).order_by('-id')
	exists   = qs.exists()
	

	
	if exists:
		new_slug = '%s-%s' %(slug,ranEX)
		return create_slug(instance,new_slug=new_slug)
	return slug



def pre_save_post_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)




pre_save.connect(pre_save_post_receiver,sender=Post)
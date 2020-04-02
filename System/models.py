from django.db import models

from django.contrib.auth.models import User

from PIL import Image

from django.utils import timezone

from django.shortcuts import reverse

from django.db.models.signals import pre_save

from django.utils.text import slugify

import random

from random import randint

from django.conf import settings

import io
from django.core.files.storage import default_storage as storage


class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	image            = models.ImageField(default='default.jpg',upload_to='profile_pics')
	background_image = models.ImageField(default='default_background.jpg',upload_to='profile_pics_background')
	background_image_low = models.ImageField(default='b_img_low.png',upload_to='profile_pics_background')
	description = models.TextField(max_length=250,blank=True,null=True)
	slug        = models.SlugField(unique=True)
	veryfied = models.BooleanField(default=False)

	followers = models.ManyToManyField("Profile",blank=True,related_name='followers1')
	following = models.ManyToManyField("Profile",blank=True,related_name='following1')

	friends = models.ManyToManyField("Profile",blank=True,related_name='friends1')
	to_user = models.ManyToManyField("Profile",blank=True,related_name='to_user1')
	from_user = models.ManyToManyField("Profile",blank=True,related_name='from_user1')

	facebock  = models.URLField(null=True,blank=True)
	twitter   = models.URLField(null=True,blank=True)
	instagram = models.URLField(null=True,blank=True)
	linkedin  = models.URLField(null=True,blank=True)
	youtube   = models.URLField(null=True,blank=True)
	email     = models.EmailField(null=True,blank=True)

	reddit    = models.URLField(null=True,blank=True)
	snapchat  = models.URLField(null=True,blank=True)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img_read = storage.open(self.image.name, 'r')
		img = Image.open(img_read)
		#img_2 = Image.open(StringIO.StringIO(img_read))


		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			in_mem_file = io.BytesIO()

			try:
				img.save(in_mem_file, format='JPEG')
			except:
				img.save(in_mem_file, format='PNG')
			img_write = storage.open(self.image.name, 'w+')
			img_write.write(in_mem_file.getvalue())
			img_write.close()
		else:
			in_mem_file = io.BytesIO()
			try:
				img.save(in_mem_file, format='JPEG')
			except:
				img.save(in_mem_file, format='PNG')

			img_write = storage.open(self.image.name, 'w+')
			img_write.write(in_mem_file.getvalue())
			img_write.close()
		img_read.close()

		b_img_read = storage.open(self.background_image.name, 'r')
		b_img = Image.open(b_img_read)


		if b_img.height > 900 or b_img.width > 900:
			output_size = (900, 900)
			b_img.thumbnail(output_size)
			in_mem_file = io.BytesIO()
			try:
				b_img.save(in_mem_file, format='JPEG')
			except:
				b_img.save(in_mem_file, format='PNG')
			b_img_write = storage.open(self.background_image.name, 'w+')
			b_img_write.write(in_mem_file.getvalue())
			b_img_write.close()
		else:
			in_mem_file = io.BytesIO()
			try:
				b_img.save(in_mem_file, format='JPEG')
			except:
				b_img.save(in_mem_file, format='PNG')

			b_img_write = storage.open(self.background_image.name, 'w+')
			b_img_write.write(in_mem_file.getvalue())
			b_img_write.close()

		b_img_read.close()



	def get_absolute_url(self):
		return reverse("user-detail",kwargs={'slug':self.slug})

	def load_more_post_url(self):
		return reverse("load-more-post",kwargs={'slug':self.slug})

	def api_follow_url(self):
		return reverse('follow-api',kwargs={'slug':self.slug})

	def load_more_posts_url(self):
		return reverse('load-more-post-user',kwargs={'slug':self.slug})


class Following(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='from_user1',on_delete=models.CASCADE)
	to_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='to_user1',on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-timestamp"]


	def __str__(self):
		return "From {}, to {}".format(self.from_user.username,self.to_user.username)

	
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

	abc7 = 'AbBcDauxVdsddsdsdsg9aSJsS9gSfx2gggf0It8pAggfgfddsSGCs8jhjhjgDs2YBs0ixS'

	rabc7 = random.choice(abc7)

	abc8 = 'AbBcDauxVdasdadddsdsdsdsdfddasdadasdfx20It8pAddsSGCs8gDdsddsds55462213Ds2YBs0ixS'

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



	abcExtra = 'AsDSDSdhi6SUDSjdoId32siaofsdfdsud31213123siu3hu423mkujnyhtbvgfcqyfhs4iuhfiuf5432424gushfsoshaoishfuoigus'

	ranEX = random.choice(abcExtra)



	slug     =  slugify(ran)
	if new_slug is not None:
		slug = new_slug

	qs       = Profile.objects.filter(slug=slug).order_by('-id')
	exists   = qs.exists()
	

	
	if exists:
		new_slug = '%s-%s' %(slug,ranEX)
		return create_slug(instance,new_slug=new_slug)
	return slug


def pre_save_profile_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)




pre_save.connect(pre_save_profile_receiver,sender=Profile)
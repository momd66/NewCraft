from django.contrib import admin

from .models import Post,RecommendPost

admin.site.register(Post)
admin.site.register(RecommendPost)
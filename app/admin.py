#coding:utf-8
from django.contrib import admin
from app.models import People, Article, Comment, UserProfile
# Register your models here.

admin.site.register(People)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(UserProfile)
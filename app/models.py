#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Factory

# Create your models here.
class People(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    job = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    CHOICES = (
        ('female', '女'),
        ('male', '男'),
        ('secret', '保密'),
    )
    sex = models.CharField(choices=CHOICES, max_length=10, null=True)
    profile_image = models.FileField(upload_to='profile_image', null=True, blank=True)
    last_visit_dt = models.DateTimeField(null=True, blank=True)
    full_information = models.BooleanField(default=False)

    def __str__(self):
        return str(self.belong_to)

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.CharField(null=True, blank=True, max_length=500)
    img = models.FileField(upload_to='art_img', null=True)
    content = models.TextField(null=True, blank=True)
    put_time = models.DateField(auto_now=True)
    CHOICES = (
        ('tech', 'Tech'),
        ('life', 'Life'),
    )
    tag = models.CharField(blank=True, max_length=5, choices=CHOICES)
    click_rate = models.PositiveIntegerField(default=0)
    collector = models.ManyToManyField(to=UserProfile, related_name='collections')

    def __str__(self):
        return self.header


class Comment(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50)
    comment = models.TextField()
    article = models.ForeignKey(to=Article, related_name='comments', blank=True)

    def __str__(self):
        return self.comment

class Tikcet(models.Model):
    voter = models.ForeignKey(to=UserProfile, related_name='voted_tickets')
    article = models.ForeignKey(to=Article, related_name='tickets')
    CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('normal', 'Normal'),
    )
    vote = models.CharField(choices=CHOICES, max_length=10)

    def __str__(self):
        return str(self.id)



import random
# users = User.objects.all()
# a = Article.objects.get(id=2)
# for user in range(len(users)):
#     profile = UserProfile.objects.get_or_create(belong_to=user)
#     profile.collections.add(a)
#     a.save()
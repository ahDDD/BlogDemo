#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from faker import Factory

# Create your models here.
class People(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    job = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.header

class Comment(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50)
    comment = models.TextField()
    article = models.ForeignKey(to=Article, related_name='comments', blank=True)

    def __str__(self):
        return self.comment

class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    profile_image = models.FileField(upload_to='profile_image', null=True, blank=True)
    last_visit_dt = models.DateTimeField(null=True, blank=True)


# CHOICES = (
#         'tech',
#         'life',
#     )
#
# import random
# fake = Factory.create()
# for _ in range(100):
#     a = Article(
#         header=fake.text(max_nb_chars=50),
#         content=fake.text(max_nb_chars=3000),
#         tag=random.choice(CHOICES),
#         click_rate=int(random.uniform(1, 9999)),
#     )
#     a.save()
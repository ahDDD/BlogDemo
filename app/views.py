# coding=utf-8
from django.shortcuts import render, redirect, Http404
from app.models import People, Article, Comment, UserProfile, Tikcet
from app.forms import CommentForm, LoginForm, UserProfileForm, PasswordForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import Context, Template
from django.db.models import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from django.contrib.auth.decorators import login_required

from pprint import pprint
import datetime

# RsST
from django.views.decorators.csrf import csrf_exempt
from app.serializers import ArticleModelSerializer, ArticlesModelSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

# Create your views here.

def index(request, tag=None, sort=None):

    # print type(request.session['ttl'])
    # pprint(dir(request.session))
    if tag:
        articles = Article.objects.filter(tag=tag)
    else:
        articles = Article.objects.all()

    if sort:
        articles = articles.order_by('click_rate')

    context = {}
    paginator = Paginator(articles, 10)
    try:
        articles = paginator.page(request.GET.get('page'))
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
        # raise Http404('Empty!')
    except PageNotAnInteger:
        articles = paginator.page(1)
    if request.user.is_authenticated():
        context['user'] = UserProfile.objects.get(belong_to=request.user)
    context['paginator'] = paginator
    context['articles'] = articles
    return render(request, 'l7h2.html', context)

def detail(request, art_id, tag=None, error_form=None):
    if datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') > request.session['ttl']:
        if UserProfile.objects.get(belong_to=request.user).full_information is False:
            return redirect(to='complete')
    context = {}
    article = Article.objects.get(id=art_id)
    user_profile = request.user.profile
    context['collector'] = article.collector.all()
    context['collected'] = True if article in user_profile.collections.all() else False
    context['got_it'] = Tikcet.objects.filter(article=article).filter(vote='like').count()
    try:
        ticket = Tikcet.objects.get(article=article, voter=user_profile)
        context['ticket'] = ticket
    except ObjectDoesNotExist:
        pass
    if tag:
        pre = Article.objects.filter(tag=tag).filter(id__lt=art_id).order_by('-id').first()
        nex = Article.objects.filter(tag=tag).filter(id__gt=art_id).order_by('id').first()
        pre,nex = map(edge, (pre,nex))
    else:
        pre = Article.objects.filter(id__lt=art_id).order_by('-id').first()
        nex = Article.objects.filter(id__gt=art_id).order_by('id').first()
        pre,nex = map(edge, (pre,nex))
    context['pre'] = pre
    context['nex'] = nex

    form = CommentForm()
    if error_form:
        context['form'] = error_form
    else:
        context['form'] = form
    context['article'] = article
    return render(request, 'l8h2.html', context)

def detail_voter(request, art_id, tag=None, error_form=None):
    user_profile = request.user.profile
    article = Article.objects.get(id=art_id)

    if request.POST.get('collect', False):
        if article in user_profile.collections.all():
            user_profile.collections.remove(article)
        else:
            user_profile.collections.add(article)
    try:
        vote = request.POST['vote']
        ticket = Tikcet.objects.get(article=article, voter=user_profile)
        ticket.vote = vote
        ticket.save()
    except ObjectDoesNotExist:
        new_ticket = Tikcet(voter_id=user_profile.id, article_id=art_id, vote=request.POST['vote'])
        new_ticket.save()
    except MultiValueDictKeyError:
        pass

    return redirect(to='detail', art_id=art_id, tag=tag)

def comment_post(request, art_id, tag=None, error_form=None):
    if datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') > request.session['ttl']:
        if UserProfile.objects.get(belong_to=request.user).full_information is False:
            return redirect(to='complete')
    form = CommentForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        c = Comment(name=name, comment=comment, article_id=art_id)
        c.save()
    else:
        return detail(request, art_id, tag, error_form=form)
    return redirect(to='detail', art_id=art_id , tag=tag)

def index_login(request):
    context = {}
    if request.method == 'GET':
        form = AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = UserProfile.objects.get(belong_to=form.get_user())
            user.last_visit_dt = form.get_user().last_login
            user.save()
            login(request, form.get_user())

            # request.session['ttl'] = form.get_user().last_login.isoformat()
            print 'view is on'
            return redirect(to='index', tag='', sort='')
    context['form'] = form
    return render(request, 'login.html', context)

def index_register(request):
    context = {}
    if request.method == 'GET':
        form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='login')
    context['form'] = form
    return render(request, 'login.html', context)

def index_logout(request):
    logout(request)
    return redirect(to='login')

def complete(request):
    context = {}
    return render(request, 'complete.html', context)

@login_required
def profile(request, error_up_form=None, error_pwd_form=None):
    context = {}
    if error_up_form:
        context['profile_form'] = error_up_form
    else:
        context['profile_form'] = UserProfileForm
    if error_pwd_form:
        print 'here'
        print  error_pwd_form.errors
        context['pwd_form'] = error_pwd_form
    else:
        context['pwd_form'] = PasswordForm
    context['tab'] = request.session.get('tab')
    return render(request, 'profile.html', context)

def profile_post(request):
    request.session['tab'] = 'tab1'
    profile = request.user.profile
    form = UserProfileForm(request.POST, instance=profile)
    if form.is_valid():
        user_profile = form.save()
        user_profile.save()
    return redirect(to='profile')

def pwd_post(request):
    request.session['tab'] = 'tab2'
    form = PasswordForm(request.POST)
    print request.POST.get('oldpassword', '')
    print request.user
    print form.is_valid()
    if form.is_valid():
        oldpassword = request.POST.get('oldpassword', '')
        print request.user.check_password(oldpassword)
        if request.user.check_password(oldpassword):
            newpassword = request.POST.get('newpassword1', '')
            request.user.set_password(newpassword)
            request.user.save()
        else:
            form.errors['oldpassword'] = ErrorList([u'原密码不正确啊'])
            return profile(request, error_pwd_form=form)
    else:
        return profile(request, error_pwd_form=form)
    return redirect(to='profile')

def my(request):
    context = {}
    context['articles'] = request.user.profile.collections.all()
    return render(request, 'my.html', context)


def edge(obj):
    try:
        obj = obj.id
    except AttributeError:
        obj = 0
    return obj

def is_ttd(ttl):
    if datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') > ttl:
        return redirect(to='complete')


# ReST

@api_view(['GET'])
def article_list(request):
    """
    默认在GET情况下
    """
    articles = Article.objects.all()
    paginator = Paginator(articles, 5)
    try:
        articles =  paginator.page(request.GET.get('page'))
    except EmptyPage:
        articles =  paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        articles =  paginator.page(1)
    serializer = ArticleModelSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleModelSerializer(article)
        return Response(serializer.data)


class ArticleList(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleModelSerializer(articles, many=True)
        return Response(serializer.data)

class ArticleDetail(APIView):

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleModelSerializer(article)
        return Response(serializer.data)

class ArticlePage(APIView):

    def get_object(self, page_num):
        articles = Article.objects.all()
        paginator = Paginator(articles, 10)
        try:
            articles = paginator.page(page_num)
            return articles
        except EmptyPage:
            return paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            return paginator.page(1)

    def get(self, request):
        articles = self.get_object(page_num=request.GET.get('page'))
        serializer = ArticlesModelSerializer(articles, many=True)
        return Response(serializer.data)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def page_range(self):
        value = [i for i in range(1,self.page.paginator.num_pages + 1)]
        if self.page.number - 3 < 0:
            lists = value[:5]
        elif self.page.number + 2 > len(value):
            lists = value[-5:]
        else:
            lists = value[self.page.number-3:self.page.number+2]
        return lists

    def get_paginated_response(self, data):
        p_r = self.page_range()
        return Response(
            OrderedDict([
                ('range', p_r),
                ('number', self.page.number),
                ('total_count', self.page.paginator.count),
                ('page_count', self.page.paginator.num_pages),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('results', data)
            ])
        )


class ArticleListGenerics(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticlesModelSerializer
    pagination_class = StandardResultsSetPagination

class ArticleDetailGen(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
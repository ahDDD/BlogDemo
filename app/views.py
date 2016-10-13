# coding=utf-8
from django.shortcuts import render, HttpResponse, redirect, Http404
from app.models import People, Article, Comment, UserProfile
from app.forms import CommentForm, LoginForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import Context, Template

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from pprint import pprint
# Create your views here.

def index(request, tag=None, sort=None):

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
    print request.user
    context['user'] = UserProfile.objects.get(belong_to=request.user)
    context['paginator'] = paginator
    context['articles'] = articles
    return render(request, 'l7h2.html', context)

def detail(request, art_id, tag=None, error_form=None):
    context = {}
    article = Article.objects.get(id=art_id)
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

def comment_post(request, art_id, tag=None):
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
            print form.get_user().last_login
            print dir(form.get_user())
            login(request, form.get_user())
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
    print (dir(request))
    logout(request)
    return redirect(to='login')

def edge(obj):
    try:
        obj = obj.id
    except AttributeError:
        obj = 0
    return obj
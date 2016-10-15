# coding=utf-8
from django.shortcuts import render, HttpResponse, redirect, Http404
from app.models import People, Article, Comment, UserProfile, Tikcet
from app.forms import CommentForm, LoginForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import Context, Template
from django.db.models import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from pprint import pprint
import datetime
# Create your views here.

def index(request, tag=None, sort=None):
    if datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') > request.session['ttl']:
        if UserProfile.objects.get(belong_to=request.user).full_information is False:
            return redirect(to='complete')

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
            ttl = form.get_user().last_login + datetime.timedelta(minutes=5)
            ttl = ttl.strftime('%Y-%m-%d %H:%M:%S')
            request.session['ttl'] = ttl
            # request.session['ttl'] = form.get_user().last_login.isoformat()
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

def edge(obj):
    try:
        obj = obj.id
    except AttributeError:
        obj = 0
    return obj

def is_ttd(ttl):
    if datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') > ttl:
        return redirect(to='complete')
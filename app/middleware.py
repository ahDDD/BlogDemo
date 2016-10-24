#coding=utf-8
from django.utils.deprecation import MiddlewareMixin
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from app.models import UserProfile
from django.shortcuts import redirect

import datetime


class ToolMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # 绑定UserProfile
        try:
            # register的方法后才存在User,所以放在response中间件中
            user = User.objects.get(username=request.POST['username'])
            UserProfile.objects.get_or_create(belong_to=user)

            # login方法后才有本次的登录时间,所以放在response中,移至此处是防止在admin登录时没有记录ttl(虽然一般user并不能登录admin)
            ttl = user.date_joined + datetime.timedelta(minutes=5)
            ttl = ttl.strftime('%Y-%m-%d %H:%M:%S')
            request.session['ttl'] = ttl
        except TypeError:
            pass
        except MultiValueDictKeyError:
            pass

        # if request.user.is_authenticated:
        #     if datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') > request.session['ttl']:
        #         if UserProfile.objects.get(belong_to=request.user).full_information is False:
        #             return redirect(to='complete')

        return response
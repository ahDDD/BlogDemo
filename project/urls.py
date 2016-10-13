"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app.views import index, detail, comment_post, index_login, index_register, index_logout
from django.contrib.auth.views import logout

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/(?P<tag>\w*)(?P<sort>/*\w*)$', index, name='index'),
    url(r'^detail/(?P<art_id>\d+)/(?P<tag>\w*)$', detail, name='comment'),
    url(r'^comment/(?P<art_id>\d+)(?P<tag>/*\w*)/post$', comment_post, name='comment_post'),
    url(r'^login$', index_login, name='login'),
    url(r'^register$', index_register, name='register'),
    url(r'^logout$', logout, {'next_page': '/login'}, name='logout'),
    url(r'^logout$', index_logout, name='index_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
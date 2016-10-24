# ReST
from django.conf.urls import url
from app.views import article_list, article_detail

urlpatterns = [
    url(r'^articles/$', article_list),
    url(r'^articles/(?P<pk>\d+)/$', article_detail),
]
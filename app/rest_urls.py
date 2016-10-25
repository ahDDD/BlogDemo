# ReST
from django.conf.urls import url
from app.views import article_list, article_detail
from app.views import ArticleList, ArticleDetail
from app.views import ArticleListGenerics, ArticleDetailGen
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^articles/$', ArticleListGenerics.as_view()),
    url(r'^articles/(?P<pk>\d+)/$', article_detail),
    url(r'^articles1/(?P<pk>\d+)/$', ArticleDetail.as_view()),
    url(r'^articles2/(?P<pk>\d+)/$', ArticleDetailGen.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
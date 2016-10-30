# ReST
from django.conf.urls import url
from app.views import article_list, article_detail
from app.views import ArticleList, ArticleDetail, ArticlePage
from app.views import ArticleListGenerics, ArticleDetailGen
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^articles/$', ArticleListGenerics.as_view()),
    url(r'^articles1/$', ArticlePage.as_view()),
    url(r'^article/(?P<pk>\d+)/$', ArticleDetail.as_view()),
    url(r'^article1/(?P<pk>\d+)/$', ArticleDetailGen.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
__author__ = 'rayleigh'

from django.conf.urls import *
from views import RootArticleView, ArticleView

urlpatterns = patterns('wiking.views',
   (r'^project/(?P<project_slug>[a-zA-Z0-9_]+)/$', ArticleView.index),
   (r'^project/(?P<project_slug>[a-zA-Z0-9_]+)/new$', ArticleView.new),
   (r'^project/(?P<project_slug>[a-zA-Z0-9_]+)/(?P<article_slug>[a-zA-Z0-9_\(\)-/]+)/edit$', ArticleView.edit),
   (r'^project/(?P<project_slug>[a-zA-Z0-9_]+)/(?P<article_slug>[a-zA-Z0-9_\(\)-/]+)/delete$', ArticleView.delete),
   (r'^project/(?P<project_slug>[a-zA-Z0-9_]+)/(?P<article_slug>[a-zA-Z0-9_\(\)-/]+)/$', ArticleView.show),
   (r'^project/(?P<project_slug>[a-zA-Z0-9_]+)/$', ArticleView.index),
   (r'^new$', RootArticleView.new),
   (r'^(?P<article_slug>[a-zA-Z0-9_\(\)-/]+)/edit$', RootArticleView.edit),
   (r'^(?P<article_slug>[a-zA-Z0-9_\(\)-/]+)/delete$', RootArticleView.delete),
   (r'^(?P<article_slug>[a-zA-Z0-9_\(\)-/]+)/$', RootArticleView.show),
   (r'^$', RootArticleView.index),
)

__author__ = 'rayleigh'

from django.conf.urls import *
from views import ArticleView

urlpatterns = patterns('wiking.views',
   (r'^project/(?P<project_id>[0-9]+)/$', ArticleView.index),
   (r'^project/(?P<project_id>[0-9]+)/new$', ArticleView.new),
   (r'^project/(?P<project_id>[0-9]+)/create$', ArticleView.create),
   (r'^project/(?P<project_id>[0-9]+)/(?P<article_slug>[a-zA-Z0-9_\(\)-]+)/edit$', ArticleView.edit),
   (r'^project/(?P<project_id>[0-9]+)/(?P<article_slug>[a-zA-Z0-9_\(\)-]+)/update$', ArticleView.update),
   (r'^project/(?P<project_id>[0-9]+)/(?P<article_slug>[a-zA-Z0-9_\(\)-]+)/delete$', ArticleView.delete),
   (r'^project/(?P<project_id>[0-9]+)/(?P<article_slug>[a-zA-Z0-9_\(\)-]+)$', ArticleView.show),
)

__author__ = 'rayleigh'
from django.http import HttpResponse
import json
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.shortcuts import render_to_response
from wiking.services.articles import ArticleService


class RootArticleView:
    def __init__(self):
        pass

    @staticmethod
    @require_safe
    def new(request):
        return render_to_response('base.html', {'title': 'RootArticle new'}, content_type='text/html')

    @staticmethod
    @require_POST
    def create(request):
        return render_to_response('base.html', {'title': 'RootArticle create'}, content_type='text/html')

    @staticmethod
    @require_safe
    def edit(request, article_slug):
        return render_to_response('base.html',
                                  {'title': 'RootArticle edit:' + article_slug},
                                  content_type='text/html')

    @staticmethod
    @require_POST
    def update(request, article_slug):
        return render_to_response('base.html',
                                  {'title': 'RootArticle update:' + article_slug},
                                  content_type='text/html')

    @staticmethod
    @require_POST
    def delete(request, article_slug):
        return render_to_response('base.html',
                                  {'title': 'RootArticle delete:' + article_slug},
                                  content_type='text/html')

    @staticmethod
    @require_safe
    def index(request):
        from PManager.viewsExt.headers import initGlobals
        header_values = initGlobals(request)
        return render_to_response('base.html',
                                  {'title': 'Root Wiking index', 'main': header_values, 'user': request.user},
                                  content_type='text/html')

    @staticmethod
    @require_safe
    def show(request, article_slug):
        return render_to_response('base.html',
                                  {'title': 'RootArticle:' + article_slug},
                                  content_type='text/html')



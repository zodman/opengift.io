from django.core.exceptions import PermissionDenied

__author__ = 'rayleigh'
from django.http import HttpResponse, HttpResponseRedirect, Http404
import json
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.shortcuts import render_to_response
from wiking.services.articles import ArticleService
from wiking.views.forms import ArticleForm
from PManager.viewsExt.headers import initGlobals


class RootArticleView:
    def __init__(self):
        pass

    @staticmethod
    @require_http_methods(['GET', 'POST', 'HEAD'])
    def new(request):
        slug = request.GET.get('slug')
        #todo: should check slug by regex
        if not slug or len(slug) < 1:
            raise Http404
        parent, slug, articles, error = ArticleService.parse_slug(slug)
        if error == ArticleService.PATH_NOT_FIND:
            raise Http404
        response = RootArticleView.__env(request)
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            response['new_form'] = False
            if form.is_valid():
                data = form.cleaned_data
                data['parent'] = parent
                article = ArticleService.create_article(data, request.user)
                return HttpResponseRedirect(ArticleService.get_absolute_url(article, articles))
        else:
            form = ArticleForm({'slug': slug})
            response['new_form'] = True
        response['form'] = form
        return render_to_response('articles/new.html', response, content_type='text/html')

    @staticmethod
    @require_http_methods(['GET', 'POST', 'HEAD'])
    def edit(request, article_slug):
        parent, slug, articles, error = ArticleService.parse_slug(article_slug)
        article = ArticleService.get_article(parent, slug)
        if error == ArticleService.PATH_NOT_FIND:
            raise Http404
        response = RootArticleView.__env(request)
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                data['parent'] = parent
                article = ArticleService.update_article(article, data, request.user)
                return HttpResponseRedirect(ArticleService.get_absolute_url(article, articles))
        else:
            form_data = ArticleService.get_form_data(article)
            form = ArticleForm(form_data)
        response['form'] = form
        response['show_url'] = ArticleService.get_absolute_url(article, articles)
        return render_to_response('articles/edit.html',
                                  response,
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
        response = RootArticleView.__env(request)
        response['articles'] = ArticleService.articles(project__isnull=True, level=0)
        return render_to_response('articles/index.html',
                                  response,
                                  content_type='text/html')

    @staticmethod
    @require_safe
    def show(request, article_slug):
        parent, slug, articles, error = ArticleService.parse_slug(article_slug)
        if error == ArticleService.PATH_NOT_FIND:
            raise Http404
        data = RootArticleView.__env(request)
        data['parent'] = parent
        data['breadcrumbs'] = ArticleService.get_breadcrumbs(articles)
        article = ArticleService.get_article(parent, slug)
        if not ArticleService.can_read(article, request.user):
            raise PermissionDenied
        data['can_write'] = ArticleService.can_write(article, request.user)
        if not article:
            return HttpResponseRedirect(ArticleService.get_create_path(article_slug))
        data['article'] = article
        return render_to_response('articles/show.html',
                                  data,
                                  content_type='text/html')

    @staticmethod
    def __env(request):
        data = dict()
        data['user'] = request.user
        data['main'] = initGlobals(request)
        return data

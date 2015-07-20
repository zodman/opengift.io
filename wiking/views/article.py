from django.core.exceptions import PermissionDenied

__author__ = 'rayleigh'
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.shortcuts import render_to_response
from wiking.services.articles import ArticleService
from wiking.views.forms import ArticleForm
from PManager.viewsExt.headers import initGlobals
from PManager.services.projects import get_project_by_id


class ArticleView:
    def __init__(self):
        pass

    @staticmethod
    @require_http_methods(['GET', 'POST', 'HEAD'])
    def new(request, project_slug=None):
        project = get_project_by_id(project_slug)
        raw_slug = request.GET.get('slug')
        #todo: should check slug by regex
        if not ArticleService.can_create(request.user, project):
            raise PermissionDenied
        if not raw_slug or len(raw_slug) < 1:
            raise Http404
        parent, slug, articles, error = ArticleService.parse_slug(raw_slug, project)
        if error == ArticleService.PATH_NOT_FIND:
            raise Http404
        article = ArticleService.get_article(parent, slug, project)
        if article:
            return HttpResponseRedirect(ArticleService.get_absolute_url(article, articles))
        response = ArticleView.__env(request)
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            response['new_form'] = False
            if form.is_valid():
                data = form.cleaned_data
                data['parent'] = parent
                data['project'] = project
                article = ArticleService.create_article(data, request.user)
                return HttpResponseRedirect(ArticleService.get_absolute_url(article, articles))
        else:
            form = ArticleForm({'slug': slug})
            response['new_form'] = True
        response['form'] = form
        return render_to_response('articles/new.html', response, content_type='text/html')

    @staticmethod
    @require_http_methods(['GET', 'POST', 'HEAD'])
    def edit(request, article_slug, project_slug=None):
        project = get_project_by_id(project_slug)
        parent, slug, articles, error = ArticleService.parse_slug(article_slug, project)
        article = ArticleService.get_article(parent, slug, project)
        if error == ArticleService.PATH_NOT_FIND:
            raise Http404
        response = ArticleView.__env(request)
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
    def delete(request, article_slug, project_slug=None):
        parent, slug, articles, error = ArticleService.parse_slug(article_slug)
        if error == ArticleService.PATH_NOT_FIND:
            raise Http404
        article = ArticleService.get_article(parent, slug)
        if not ArticleService.can_write(article, request.user):
            raise PermissionDenied
        if not article:
            raise Http404
        path = ArticleService.get_parent_path(article, articles)
        article.deleted = True
        article.save()
        return HttpResponseRedirect(path)

    @staticmethod
    @require_safe
    def index(request, project_slug=None):
        response = ArticleView.__env(request)
        project = get_project_by_id(project_slug)
        if project is None:
            response['articles'] = ArticleService.articles(project__isnull=True, level=0, deleted=False)
        else:
            response['articles'] = ArticleService.articles(project__isnull=False, level=0,
                                                           deleted=False, project=project)
        return render_to_response('articles/index.html',
                                  response,
                                  content_type='text/html')

    @staticmethod
    @require_safe
    def show(request, article_slug, project_slug=None):
        project = get_project_by_id(project_slug)
        parent, slug, articles, error = ArticleService.parse_slug(article_slug, project)
        if error == ArticleService.PATH_NOT_FIND:
            raise Http404
        data = ArticleView.__env(request)
        data['parent'] = parent
        data['breadcrumbs'] = ArticleService.get_breadcrumbs(articles)
        data['project'] = project
        article = ArticleService.get_article(parent, slug, project)
        if not ArticleService.can_read(article, request.user):
            raise PermissionDenied
        data['can_write'] = ArticleService.can_write(article, request.user)
        if not article:
            return HttpResponseRedirect(ArticleService.get_create_path(article_slug, project))
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

__author__ = 'rayleigh'
from django.http import HttpResponse
import json
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.shortcuts import render_to_response
from wiking.services.articles import ArticleService

class ArticleView:
    def __init__(self):
        pass

    @staticmethod
    @require_safe
    def new(request, project_slug):
        #view for the new form
        slug = request.GET.get('slug', '')
        return render_to_response('base.html',
                                  {'title': 'This is the new response; The slug is :'
                                      + slug + '; Project id is: ' + project_slug},
                                  content_type='text/html')

    @staticmethod
    @require_POST
    def create(request, project_slug):
        #create article from the new form
        slug = request.GET.get('slug', '')
        data = request.POST
        data_json = json.dumps(data)
        return render_to_response('base.html',
                                  {'title': 'This is the create response; The slug is :'
                                      + slug + '; Project id is: ' + project_slug + '; Data is: ' + data_json},
                                  content_type='text/html')

    @staticmethod
    @require_safe
    def edit(request, project_slug, article_slug):
        #create edit form
        return render_to_response('base.html',
                                  {'title': 'This is the edit response; The slug is :'
                                      + article_slug + '; Project id is: ' + project_slug},
                                  content_type='text/html')

    @staticmethod
    @require_POST
    def update(request, project_slug, article_slug):
        #save from edit form, save revision as well
        return render_to_response('base.html',
                                  {'title': 'This is the update response; The slug is :'
                                      + article_slug + '; Project id is: ' + project_slug},
                                  content_type='text/html')

    @staticmethod
    @require_POST
    def delete(request, project_slug, article_slug):
        #soft deletes an article? remove article, but saves revisions
        return render_to_response('base.html',
                                  {'title': 'This is the delete response; The slug is :'
                                      + article_slug + '; Project id is: ' + project_slug},
                                  content_type='text/html')

    @staticmethod
    @require_safe
    def index(request, project_slug):
        #show list of articles
        return render_to_response('base.html',
                                  {'title': 'This is the index response; Project id is: ' + project_slug},
                                  content_type='text/html')

    @staticmethod
    @require_safe
    def show(request, project_slug, article_slug):
        #show article
        return render_to_response('base.html',
                                  {'title': 'This is the show response; The slug is :'
                                      + article_slug + '; Project id is: ' + project_slug},
                                  content_type='text/html')



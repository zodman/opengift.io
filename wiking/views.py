from django.http import HttpResponse
import json
from services.articles import ArticleService


class RootArticleView:
    def __init__(self):
        pass

    @staticmethod
    def new(request):
        return HttpResponse('RootArticle new')

    @staticmethod
    def create(request):
        return HttpResponse('RootArticle create')

    @staticmethod
    def edit(request, article_slug):
        return HttpResponse('RootArticle edit:' + article_slug)

    @staticmethod
    def update(request, article_slug):
        return HttpResponse('RootArticle update:' + article_slug)

    @staticmethod
    def delete(request, article_slug):
        return HttpResponse('RootArticle delete:' + article_slug)

    @staticmethod
    def index(request):
        return HttpResponse('Root Wiking index')

    @staticmethod
    def show(request, article_slug):
        return HttpResponse('RootArticle:' + article_slug)


class ArticleView(RootArticleView):
    def __init__(self):
        pass

    @staticmethod
    def new(request, project_slug):
        #view for the new form
        slug = request.GET.get('slug', '')
        return HttpResponse('This is the new response; The slug is :'
                            + slug + '; Project id is: ' + project_slug)

    @staticmethod
    def create(request, project_slug):
        #create article from the new form
        slug = request.GET.get('slug', '')
        data = request.POST
        data_json = json.dumps(data)
        return HttpResponse('This is the create response; The slug is :'
                            + slug + '; Project id is: ' + project_slug + '; Data is: ' + data_json)

    @staticmethod
    def edit(request, project_slug, article_slug):
        #create edit form
        return HttpResponse('This is the edit response; The slug is :'
                            + article_slug + '; Project id is: ' + project_slug)

    @staticmethod
    def update(request, project_slug, article_slug):
        #save from edit form, save revision as well
        return HttpResponse('This is the update response; The slug is :'
                            + article_slug + '; Project id is: ' + project_slug)

    @staticmethod
    def delete(request, project_slug, article_slug):
        #soft deletes an article? remove article, but saves revisions
        return HttpResponse('This is the delete response; The slug is :'
                            + article_slug + '; Project id is: ' + project_slug)

    @staticmethod
    def index(request, project_slug):
        #show list of articles
        return HttpResponse('This is the index response; Project id is: ' + project_slug)

    @staticmethod
    def show(request, project_slug, article_slug):
        #show article
        return HttpResponse('This is the show response; The slug is :'
                            + article_slug + '; Project id is: ' + project_slug)



from django.http import HttpResponse
import json

class ArticleView:
    def __init__(self):
        pass

    @staticmethod
    def new(request, project_id):
        #view for the new form
        slug = request.GET.get('slug', '')
        return HttpResponse('This is the new response; The slug is :'
                            + slug + '; Project id is: ' + project_id)

    @staticmethod
    def create(request, project_id):
        #create article from the new form
        slug = request.GET.get('slug', '')
        data = request.POST
        data_json = json.dumps(data)
        return HttpResponse('This is the create response; The slug is :'
                            + slug + '; Project id is: ' + project_id + '; Data is: ' + data_json)

    @staticmethod
    def edit(request, project_id, article_slug):
        #create edit form
        return HttpResponse('This is the edit response; The slug is :'
                            + article_slug + '; Project id is: ' + project_id)

    @staticmethod
    def update(request, project_id, article_slug):
        #save from edit form, save revision as well
        return HttpResponse('This is the update response; The slug is :'
                            + article_slug + '; Project id is: ' + project_id)

    @staticmethod
    def delete(request, project_id, article_slug):
        #soft deletes an article? remove article, but saves revisions
        return HttpResponse('This is the delete response; The slug is :'
                            + article_slug + '; Project id is: ' + project_id)

    @staticmethod
    def index(request, project_id=None):
        #show list of articles
        return HttpResponse('This is the index response; Project id is: ' + str(project_id))

    @staticmethod
    def show(request, project_id, article_slug):
        #show article
        return HttpResponse('This is the show response; The slug is :'
                            + article_slug + '; Project id is: ' + project_id)

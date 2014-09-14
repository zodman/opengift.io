__author__ = 'Gvammer'
from django.shortcuts import HttpResponse

class userHandlers:
    @staticmethod
    def setUserOptions(request):
        action = request.REQUEST['action']
        response = u''

        return HttpResponse(response)

class usersActions:
    def set_user_roles(self):
        pass
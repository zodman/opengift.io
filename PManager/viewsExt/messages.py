__author__ = 'Gvammer'
from PManager.widgets.chat import widget as messageList
from django.shortcuts import HttpResponse
from PManager.viewsExt import headers
from PManager.models import PM_Task_Message
import json

def ajaxResponder(request):
    manager = ajaxActions(request)
    return HttpResponse(manager.process())

class ajaxActions(object):
    def __init__(self, request):
        self.request = request
        self.id = int(self.request.POST.get('id', 0))
        if 'action' in request.REQUEST:
            self.action = request.REQUEST['action']
        else:
            raise Exception('action does not exist')

    def process(self):
        if self.action != 'process' and '__' not in self.action and hasattr(self, self.action):
            return json.dumps(self.__getattribute__(self.action)())

    def setRead(self):
        if self.id > 0:
            try:
                message = PM_Task_Message.objects.get(pk=self.id)
                if message.canEdit(self.request.user):
                    message.read = True
                    message.save()
                    return 'ok'
            except PM_Task_Message.DoesNotExist:
                return 'Message not found'
        else:
            messages = PM_Task_Message.objects.filter(
                userTo=self.request.user,
                read=False
            )
            for mes in messages:
                mes.read = True
                mes.save()
            return 'ok'

    def getMessages(self):
        headerValues = headers.initGlobals(self.request)
        result = messageList(self.request, headerValues)
        return result['messages']

__author__ = 'Gvammer'
from django.shortcuts import HttpResponse
from PManager.models import PM_Milestone, PM_Project
from PManager.viewsExt.tools import templateTools

class ajaxMilestoneManager:
    def __init__(self,request):
        self.request = request

    def getRequestValue(self,key):
        if key in self.request.POST:
            return self.request.POST[key]
        else:
            return None

def ajaxMilestonesResponder(request):
    responseText = 'bad query'
    name = request.POST.get('name','')
    user = request.user
    responsible_id = request.POST.get('responsible',0)
    date = templateTools.dateTime.convertToDateTime(request.POST.get('date',''))
    id = request.POST.get('id',None)
    critically = request.POST.get('critically',2)
    action = request.POST.get('action',None)
    if not user.is_authenticated():
        return False

    try:
        project = PM_Project.objects.get(
            pk=int(request.POST.get('project',0))
        )
    except PM_Project.DoesNotExist:
        project = None

    if action == 'remove':
        if id:
            try:
                milestone = PM_Milestone.objects.get(pk=id)
                milestone.delete()
                responseText = 'removed'
            except PM_Milestone.DoesNotExist:
                pass

    elif name and date and project:
        milestone = None
        if id:
            try:
                milestone = PM_Milestone.objects.get(pk=id)
                milestone.name = name
                milestone.date = date
                milestone.project = project
            except PM_Milestone.DoesNotExist:
                pass
        else:
            milestone = PM_Milestone(name=name,date=date,project=project)

        if milestone:
            milestone.save()
            if responsible_id:
                milestone.responsible.clear()
                milestone.responsible.add(responsible_id)
            else:
                milestone.responsible.add(user)
            responseText = 'saved'

    return HttpResponse(responseText)
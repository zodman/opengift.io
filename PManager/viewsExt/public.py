__author__ = 'Gvammer'
from django.shortcuts import HttpResponse
from PManager.models import PM_User, PM_Project, PM_Project_Donation
from django.template import loader, RequestContext

class Public:
    @staticmethod
    def mainPage(request):
        c = RequestContext(request, {
            'projects_qty': PM_Project.objects.filter(public=True).count(),
            'developers_qty': PM_User.objects.filter(blockchain_wallet__isnull=False).count(),
            'donations_qty': PM_Project_Donation.objects.count(),
            'w': request.GET.get('w', '')
        })

        return HttpResponse(loader.get_template('public/index.html').render(c))
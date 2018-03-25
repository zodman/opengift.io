__author__ = 'Gvammer'
from django.shortcuts import HttpResponse, HttpResponseRedirect, Http404
from PManager.models import PM_User, PM_Project, PM_Project_Donation, PM_Task
from django.template import loader, RequestContext
from django.contrib.auth.models import User

class Public:
    @staticmethod
    def debug_on(request):
        response = HttpResponse('ok')
        return response.set_cookie('debug_mode', 'on')

    @staticmethod
    def debug_off(request):
        response = HttpResponse('ok')
        return response.set_cookie('debug_mode', 'off')

    @staticmethod
    def backerProfile(request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404

        c = RequestContext(request, {
            'need_inverse': True,
            'user': user,
            'percent': float(user.get_profile().get_donation_sum() * 100) / PM_User.level_sum[PM_User.OPENGIFTER]
        })

        return HttpResponse(loader.get_template('public/backer.html').render(c))

    @staticmethod
    def mainPage(request):
        try:
            project = PM_Project.objects.get(pk=495)
        except PM_Project.DoesNotExist:
            project = PM_Project.objects.all()[0]

        if request.GET.get('logout', None) == 'yes':
            from django.contrib.auth import logout
            logout(request)
            return HttpResponseRedirect('/pub/')

        c = RequestContext(request, {
            'projects_qty': PM_Project.objects.filter(public=True).count(),
            'developers_qty': PM_User.objects.filter(blockchain_wallet__isnull=False).count(),
            'donations_qty': PM_Project_Donation.objects.count(),
            'milestones': project.milestones.order_by('date'),
            'w': request.GET.get('w', '')
        })

        return HttpResponse(loader.get_template('public/index.html').render(c))

    @staticmethod
    def icoPage(request):
        try:
            project = PM_Project.objects.get(pk=495)
        except PM_Project.DoesNotExist:
            project = PM_Project.objects.all()[0]

        c = RequestContext(request, {
            'tasksQty': PM_Task.objects.filter(closed=True).count(),
            'projects_qty': PM_Project.objects.filter(public=True).count(),
            'developers_qty': PM_User.objects.filter(blockchain_wallet__isnull=False).count(),
            'donations_qty': PM_Project_Donation.objects.count(),
            'milestones': project.milestones.filter(closed=False, donated=False).order_by('date'),
            'w': request.GET.get('w', '')
        })

        return HttpResponse(loader.get_template('public/ico.html').render(c))
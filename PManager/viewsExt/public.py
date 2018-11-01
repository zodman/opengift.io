# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.shortcuts import HttpResponse, HttpResponseRedirect, Http404
from PManager.models import PM_User, PM_Hackathon, PM_Project, PM_Project_Donation, PM_Task
from django.template import loader, RequestContext
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class Public:
    @staticmethod
    def hackathon(request, need_inverse=False):

        now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
        hackathons = []
        for h in PM_Hackathon.objects.filter(date__lt=now).order_by('date'):
            setattr(h, 'winners', h.hackathon_winners.order_by('sort'))
            hackathons.append(h)

        c = RequestContext(request, {
            'users': PM_User.objects.filter(hackathon_reg_date=datetime.datetime(2018, 11, 3, 13, 0, 0)),
            'user_registered': request.user.is_authenticated()
                               and request.user.get_profile().hackathon_reg_date
                               and request.user.get_profile().hackathon_reg_date > now,
            'hackathons': hackathons,
            'need_inverse': need_inverse
        })
        return HttpResponse(loader.get_template('public/hackathon.html').render(c))


    @staticmethod
    def hackathon_register(request):

        c = RequestContext(request, {})
        if request.POST.get('stack', ''):
            from PManager.viewsExt.tools import emailMessage
            prof = request.user.get_profile()
            prof.hackathon_reg_date = datetime.datetime(2018, 11, 3, 13, 0, 0)
            prof.hackathon_registered = request.POST.get('stack', '')
            prof.save()

            message = emailMessage(
                'hackathon_register',
                {
                    'user': {
                        'name': request.user.first_name + ' ' + request.user.last_name
                    }
                },
                'OpenGift Hackathon registration'
            )

            message.send([request.user.email])
            # admin
            # todo: Move this method to a service
            from tracker.settings import ADMIN_EMAIL
            message.send([ADMIN_EMAIL])

            return HttpResponseRedirect('/hackathon/')

        return HttpResponse(loader.get_template('public/hackathon_register.html').render(c))

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

        bounty_fund = 0
        for d in PM_Project_Donation.objects.filter(task__closed=False, task__isnull=False):
            bounty_fund += d.sum

        donated = 0
        for d in PM_Project_Donation.objects.filter(task__isnull=True):
            donated += d.sum

        donated = int(donated)

        bounty_fund = int(bounty_fund)
        c = RequestContext(request, {
            'tasks_qty': PM_Task.objects.filter(closed=False, active=True).count(),
            'projects_qty': PM_Project.objects.filter(public=True).count(),
            'developers_qty': PM_User.objects.filter(blockchain_wallet__isnull=False).count(),
            'donated': donated,
            'bounty_fund': bounty_fund,
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

        response = HttpResponse(loader.get_template('public/ico.html').render(c))
        ref = request.GET.get('r', None)
        if ref:
            response.set_cookie('partner_id', ref)

        return response
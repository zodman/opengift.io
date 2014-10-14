# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from PManager.models import PM_User, PM_Project, PM_Tracker, PM_Task
from PManager.viewsExt.tools import emailMessage

def recall(request):
    phone = request.POST.get('phone', None)
    if phone:
        mess = emailMessage(
            'phone_recall',
            {
                'phone': phone
            },
            u'Перезвонить по этому номеру'
        )
        mess.send(['gvamm3r@gmail.com'])

    return HttpResponse(u'Спасибо! Мы перезвоним вам в течение нескольких минут.')

def register(request):
    email = request.POST.get('email', None)
    if email:
        if not emailMessage.validateEmail(email):
            return HttpResponse(u'Введите правильный email')
        if not User.objects.filter(email=email).count():
            project = PM_Project(
                name=u'Новый проект',
                description=u'Описание нового проекта',
                tracker=PM_Tracker.objects.get(pk=1),
                author=User.objects.get(pk=1)
            )

            project.save()
            user = PM_User.getOrCreateByEmail(email, project, 'client')
            user.is_staff = True
            user.save()
            project.author = user
            project.save()
            request.COOKIES["CURRENT_PROJECT"] = project.id

            prof = user.get_profile()
            prof.setRole('manager', project)
            prof.setRole('client', project, 'plan_time')
            prof.sp_price = 990
            # prof.account_total = 990
            prof.save()

            return HttpResponse(u'Спасибо за регистрацию! В ближайшее время вам на почту придет ссылка на ваш проект.<br>Обратите внимание: письмо может попасть в спам.')

        else:
            return HttpResponse(u'Такой email уже существует в системе!')

    return HttpResponse(u'Ошибка')

# def setupTracker(request):
#     USER = 'root'
#     PASS = ''
#     import subprocess
#     import MySQLdb
#     # for task in PM_Task.objects.all():
#     #     task.delete()
#     # for user in User.objects.exclude(id=1):
#     #     user.delete()
#     # for project in PM_Project.objects.exclude(id=1):
#     #     project.delete()
#     # for project in PM_Files.objects.exclude(id=1):
#     #     project.delete()
#     # for project in PM_File_Category.objects.exclude(id=1):
#     #     project.delete()
#     odb1 = MySQLdb.connect(host="localhost", user="root", passwd="")
#     cursor = odb1.cursor()
#     sql = 'CREATE DATABASE tracker_new1'
#     cursor.execute(sql)
#     odb1.close()
#     proc = subprocess.Popen(["mysql", "--user=%s" % USER, "--password=%s" % PASS, "tracker_new1"],
#                             stdin=subprocess.PIPE,
#                             stdout=subprocess.PIPE)
#     out, err = proc.communicate(file("install.sql").read())
#     return HttpResponse()
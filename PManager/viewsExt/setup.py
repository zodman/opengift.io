# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from PManager.models import PM_User, PM_Project, PM_Tracker, PM_Task

def register(request):
    email = request.POST.get('email', None)
    if email:
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
        prof = user.get_profile()
        prof.setRole('manager', project)
        prof.setRole('client', project, 'plan_time')
        prof.rate = 1000
        prof.save()

        task = PM_Task(
            name=u'Ознакомиться с системой',
            author=user,
            project=project
        )
        task.save()
        task.resp = user

    return HttpResponse(u'Спасибо за регистрацию, на вашу почту отправлено письмо с вашим паролем для доступа в систему')

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
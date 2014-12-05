# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
from django.shortcuts import HttpResponse, render
from PManager.models.users import User, PM_User
from PManager.models.keys import Key
from PManager.viewsExt import headers
from django.contrib.auth.decorators import login_required
from PManager.classes.git.gitolite_manager import GitoliteManager
import json
import re


class KeyHandler:
    def __init__(self):
        pass

    @staticmethod
    def key_remove(request, key_id):
        response_data = {"error": ""}
        key_id = int(key_id)
        if not request.user.is_authenticated:
            response_data['error'] = u'Необходимо авторизоваться'
        elif key_id <= 0:
            response_data['error'] = u'Неверный id ключа'
        elif not Key.delete(key_id, request.user):
            response_data['error'] = u'Вы не можете удалить данный ключ'
        return HttpResponse(json.dumps(response_data))

    @staticmethod
    @login_required
    def key_add(request):
        if not request.user.is_authenticated:
            return HttpResponse("{'error': 'should be authenticated'}")
        if request.method == 'POST':
            name = str(request.POST.get('key_name', ''))
            data = str(request.POST.get('key_data', ''))
            data = data.replace('\n', '').replace('\r', '')
            if len(name) > 0 and len(data) > 0:
                response_data = {'result': 'errors', 'fields': {}}
                if len(name) <= 0:
                    response_data['fields']['name'] = u'Пожалуйста введите название для ключа'
                elif len(name) > 30:
                    response_data['fields']['name'] = u'Название ключа должно быть меньше 30 символов'
                elif not re.match('^\w+$', name):
                    response_data['fields']['name'] = u'Название ключа должно состоять только из латинских букв и цифр'
                elif Key.objects.filter(user=request.user, name=name):
                    response_data['fields']['name'] = u'Ключ с данным названием уже существует'
                elif len(data) <= 0:
                    response_data['fields']['data'] = u'Пожалуйста введите ваш ключ'
                elif not re.match('ssh-rsa', data):
                    response_data['fields']['data'] = u'Пожалуйста введите валидный ключ'
                elif not GitoliteManager.check_key(data):
                    response_data['fields']['data'] = u'Пожалуйста введите валидный ключ'
                elif not Key.create(name=name, data=data, user=request.user):
                    response_data['fields']['name'] = u'Ключ не может быть создан'
                else:
                    response_data['result'] = "ok"
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return render(request, 'keys/form.html')
        return HttpResponse("")
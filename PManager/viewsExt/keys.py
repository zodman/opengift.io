# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
from django.shortcuts import HttpResponse, render
from PManager.models.users import User, PM_User
from PManager.models.keys import Key
from PManager.viewsExt import headers
from django.contrib.auth.decorators import login_required
import json
import re

class KeyHandler:
	@staticmethod
	def keyRemove(request, key_id):
		response_data = {"error":""}
		key_id = int(key_id)
		if not request.user.is_authenticated:
			response_data['error'] = u'Необходимо авторизоваться'
		elif(key_id <= 0):
			response_data['error'] = u'Неверный id ключа'
		elif(not Key.delete(key_id, request.user)):
			response_data['error'] = u'Вы не можете удалить данный ключ'			
		return HttpResponse(json.dumps(response_data))

	@staticmethod
	@login_required
	def keyAdd(request):
		if not request.user.is_authenticated:
			return HttpResponse("{'error': 'fields should be filled'}")
		if request.method == 'POST':
			name = str(request.POST.get('key_name',''))
			data = str(request.POST.get('key_data',''))
			if(len(name) > 0 and len(data) > 0):
				key = Key.create(name=name, data=data, user=request.user)
				key.save()
			else:
				response_data = {}
				response_data['result'] = 'errors'
				response_data['message'] =u'Необходимо заполнить поля'
				response_data['fields'] = {}
				if(len(name) <= 0):
					response_data['fields']['name'] = u'Пожалуйста введите название для ключа'
				elif(len(name) > 30):
					response_data['fields']['name'] = u'Название ключа должно быть меньше 30 символов'
				elif(not re.match('^\w+$', name)):
					response_data['fields']['name'] = u'Название ключа должно состоять только из латинских букв и цифр'
				elif(Key.objects.filter(user=request.user, name=name)):
					response_data['fields']['name'] = u'Ключ с данным названием уже существует'
				if(len(data) <= 0):
					response_data['fields']['data'] = u'Пожалуйста введите ваш ключ'
				elif(not re.match('^ssh-rsa', data)):
					response_data['fields']['data'] = u'Пожалуйста введите валидный ключ'
				return HttpResponse(json.dumps(response_data), content_type="application/json")
		else:
			return render(request, 'keys/form.html')
		return HttpResponse(str(key.file_path))
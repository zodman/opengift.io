# -*- coding:utf-8 -*-
__author__ = 'Tonakai'

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from PManager.classes.git.gitolite_manager import GitoliteManager

validator_isalpha = RegexValidator(r'^[\w]*$',
                             message=u'Имя ключа не должно содержать специальных символов',
                             code=u'Неверное имя ключа')

class Key(models.Model):
    name = models.CharField(max_length=32, null=False, validators=[validator_isalpha])
    file_path = models.CharField(max_length=255)
    key_data = models.TextField(null=False)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = 'PManager'

    @classmethod
    def create(cls, name, data, user):
        file_path = GitoliteManager.add_key_to_user(user, name, data)
        if (len(file_path) > 0):
            key = Key.objects.create(name=name, key_data=data, user=user, file_path=file_path)
            return key
        else:
            return False
    @classmethod
    def delete(cls, key_id, user):
        keys = cls.objects.filter(id=key_id, user=user)
        if(keys):
            for key in keys:
                GitoliteManager.remove_key_from_user(key, user)
            keys.delete()
            return True
        return False
        
# coding=utf-8
__author__ = 'Alwx'

from django.db import models
from PManager.models.tasks import PM_Project


class Conditions(models.Model):
    field_choices = (
        ('ResponseHeader', u'Заголовок ответа'),
        ('ResponseBody', u'Тело ответа'),
        ('PageHeader', u'Заголовок страницы'),
        ('PageBody', u'Тело страницы')
    )
    condition_choices = (
        ('in', u'Содержит'),
        ('not_in', u'Не содержит'),
        ('is', u'Присутствует'),
        ('is_not', u'Отсутствует')
    )

    field = models.CharField(max_length=15, choices=field_choices, verbose_name=u'Поле', blank=True, null=True)
    condition = models.CharField(max_length=6, choices=condition_choices, verbose_name=u'Условие', blank=True,
                                 null=True)
    value = models.CharField(max_length=255, verbose_name=u'Значение', blank=True, null=True)

    def __unicode__(self):
        return ' '.join([self.get_field_display(), self.get_condition_display(), self.value])

    class Meta:
        app_label = 'PManager'


class Test(models.Model):
    project = models.ForeignKey(PM_Project, related_name='tests', verbose_name=u'Проект')
    condition = models.ForeignKey(Conditions, verbose_name=u'Условие')
    passed = models.BooleanField(blank=True, verbose_name=u'Пройден')
    url = models.CharField(max_length=255, blank=True, null=True)

    def test(self):
        if self.condition:
            return True
        else:
            return False

    class Meta:
        app_label = 'PManager'

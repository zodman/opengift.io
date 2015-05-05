# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'
from PManager.services.assets import assets_get_url
from django.template import Library


register = Library()


@register.filter(name='protect')
def protect(url):
    return assets_get_url(url)
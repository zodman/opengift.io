# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
import os
import Image
from django.template import Library
from tracker import settings

register = Library()

@register.filter(name='thumbnail')
def thumbnail(file, size='200x200', resample=0):
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    basename, format = file.rsplit('.', 1)
#    print basename
    miniature = '/static/thumbnails/' + basename.rsplit('/', -1) + '_' + size + '.' +  format
    miniature_filename = os.path.join(settings.STATIC_ROOT, 'PManager'+miniature)
    miniature_url = os.path.join(settings.STATIC_URL, miniature)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
#        print '>>> debug: resizing the image to the format %s!' % size
        filename = os.path.join(settings.STATIC_ROOT, 'PManager'+file)
        if os.path.isfile(filename):
            try:
                image = Image.open(filename)
                image.thumbnail([x, y], resample) # generate a 200x200 thumbnail
                image.save(miniature_filename, image.format)
            except IOError:
                return file
    return miniature_url

@register.filter(name='protected')
def protected(url):
    return '/protected' + url
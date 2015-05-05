# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from tracker.settings import PROJECT_ROOT
from django.shortcuts import HttpResponse
from PManager.models import PM_Files
import os

def docxView(request):
    #TODO: все к херам переписать по уму
    # from docx import Document
    from shutil import copyfile
    from docx2html import convert
    def handle_image(image_id, relationship_dict):
        image_path = relationship_dict[image_id]
        # Now do something to the image. Let's move it somewhere.
        _, filename = os.path.split(image_path)
        destination_path = os.path.join(PROJECT_ROOT + 'PManager/static/upload', filename)
        copyfile(image_path, destination_path)

        # Return the `src` attribute to be used in the img tag
        return 'http://heliard.ru/static/upload/%s' % filename

    fp = request.GET.get('f', None)

    if fp:
        try:
            pm_file = PM_Files.objects.get(pk=int(fp))
            html = convert(PROJECT_ROOT + 'PManager' + str(pm_file), image_handler=handle_image)
        except PM_Files.DoesNotExist:
            pass
    return HttpResponse(html)
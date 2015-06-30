# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
from tracker.settings import PROJECT_ROOT, HTTP_ROOT_URL, MEDIA_URL, MEDIA_ROOT
from django.shortcuts import HttpResponse
from PManager.models import PM_Files
import os

def docxView(request):
    #TODO: все к херам переписать по уму
    from shutil import copyfile
    from docx2html import convert

    def handle_image(image_id, relationship_dict):
        image_path = relationship_dict[image_id]
        # Now do something to the image. Let's move it somewhere.
        _, filename = os.path.split(image_path)
        destination_path = os.path.join(MEDIA_ROOT, filename)
        copyfile(image_path, destination_path)

        # Return the `src` attribute to be used in the img tag
        return '/protected%s%s' % (MEDIA_URL, filename)

    fp = request.GET.get('f', None)

    if fp:
        try:
            pm_file = PM_Files.objects.get(pk=int(fp))
            html = convert(str(pm_file.file.path), image_handler=handle_image)
        except PM_Files.DoesNotExist:
            pass
    return HttpResponse(html)
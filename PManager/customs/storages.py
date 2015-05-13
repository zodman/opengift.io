__author__ = 'Gvammer'

from django.core.files.storage import FileSystemStorage
import os
from uuid import uuid4

def path_and_rename(path, pSubdir=False):

    def wrapper(instance, filename):
        try:
            path = path
        except UnboundLocalError:
            if pSubdir:
                path = 'PManager/static/upload/projects/'
            else:
                path = 'PManager/static/upload/'

        if pSubdir:
            path = os.path.join(path, eval(pSubdir))

        ext = filename.split('.')[-1]
        # get filename
        # if not isPasted:
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper

class MyFileStorage(FileSystemStorage):

    # This method is actually defined in Storage
    def get_available_name(self, name):
        return name # simply returns the name passed

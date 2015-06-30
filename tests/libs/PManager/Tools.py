# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'
__version__ = '0.0.1'
ROBOT_LIBRARY_SCOPE = 'GLOBAL'
ROBOT_LIBRARY_VERSION = '0.0.1'

from tracker.settings import PROJECT_ROOT
from robot.libraries.BuiltIn import BuiltIn

class Tools:
    def __init__(self):
        self.sel = BuiltIn().get_library_instance('Selenium2Library')

    @staticmethod
    def default_picture(picture=PROJECT_ROOT + "tests/uploads/default.png"):
        return picture

    @staticmethod
    def default_file(fl=PROJECT_ROOT + "tests/uploads/default"):
        return fl

    @staticmethod
    def default_docx(docx=PROJECT_ROOT + "tests/uploads/test.docx"):
        return docx

    @staticmethod
    def get_basename(path):
        return path.split('/').pop() or False

    @staticmethod
    def default_docx_with_images(docx=PROJECT_ROOT + "tests/uploads/test_imaged.docx"):
        return docx
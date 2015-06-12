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

    def get_basename(self, picture):
        return picture.split('/').pop() or False
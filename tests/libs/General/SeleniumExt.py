# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'
__version__ = '0.0.1'
ROBOT_LIBRARY_SCOPE = 'GLOBAL'
ROBOT_LIBRARY_VERSION = '0.0.1'

from robot.libraries.BuiltIn import BuiltIn


class SeleniumExt:
    def __init__(self):
        self.sel = BuiltIn().get_library_instance('Selenium2Library')

    def input_textarea(self, locator, text):
        el = self.sel._element_find(locator, True, True, tag='textarea')
        el.clear()
        el.send_keys(text)
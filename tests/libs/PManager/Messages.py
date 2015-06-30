# -*- coding:utf-8 -*-
from selenium.common.exceptions import StaleElementReferenceException

__author__ = 'Rayleigh'
__version__ = '0.0.1'
ROBOT_LIBRARY_SCOPE = 'GLOBAL'
ROBOT_LIBRARY_VERSION = '0.0.1'

from robot.libraries.BuiltIn import BuiltIn
from tests.libs.General.SeleniumExt import SeleniumExt

class Messages:

    MSG_DESCRIPTION_LOCATOR = 'css=.newMessage>div>div>[name="task_message"]'
    MSG_FILE_LOCATOR = 'css=input[type="file"][name="file"]'
    MSG_SEND_BUTTON = 'css=.sendTaskMessage'

    def __init__(self):
        self.sel = BuiltIn().get_library_instance('Selenium2Library')
        self.selenium_ext = SeleniumExt()

    def create_message(self, text='default_text', file_name=None, options=None):
        if file_name is None:
            file_name = Tools.default_file()
        if not options:
            options = []
        self.selenium_ext.input_textarea(self.MSG_DESCRIPTION_LOCATOR, text)
        if file_name is not None:
            self.sel.choose_file(self.MSG_FILE_LOCATOR, file_name)
        self.sel.click_button(self.MSG_SEND_BUTTON)
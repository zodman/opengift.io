# -*- coding:utf-8 -*-
from selenium.common.exceptions import StaleElementReferenceException

__author__ = 'Rayleigh'
__version__ = '0.0.1'
ROBOT_LIBRARY_SCOPE = 'GLOBAL'
ROBOT_LIBRARY_VERSION = '0.0.1'

from robot.libraries.BuiltIn import BuiltIn
from datetime import datetime
from selenium.webdriver.common.keys import Keys


class Tasks:
    TASK_CREATE_INPUT_LOCATOR = "css=.task-create"

    def __init__(self):
        self.sel = BuiltIn().get_library_instance('Selenium2Library')

    def create_task(self, task_name='default_task_'):
        task_name += str(datetime.now())
        self.sel.input_text(self.TASK_CREATE_INPUT_LOCATOR, task_name + Keys.ENTER)
        self.sel.wait_until_page_contains_element("link=" + task_name)
        return task_name

    def get_task_url(self, task_name):
        el = self.sel._element_find("partial link=" + task_name, True, True, tag='a')
        return el.get_attribute('href')

    def get_task_id(self, task_name):
        el = self.sel._element_find("partial link=" + task_name, True, True, tag='a')
        el = el.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
        return el.get_attribute('id')

    def task_should_be_present(self, task_name):
        el = self.sel._element_find("partial link=" + task_name, True, False, tag='a')
        if not el:
            raise AssertionError("Page should contain task '%s' "
                                 "but it did not" % task_name)

    def task_should_not_be_present(self, task_name):
        try:
            el = self.sel._element_find("partial link=" + task_name, True, False, tag='a')
        except StaleElementReferenceException:
            return
        raise AssertionError("Page should not contain task '%s' "
                                 "but it did" % task_name)
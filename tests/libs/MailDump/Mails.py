# -*- coding:utf-8 -*-
import time

__author__ = 'Rayleigh'
__version__ = '0.0.1'
ROBOT_LIBRARY_SCOPE = 'GLOBAL'
ROBOT_LIBRARY_VERSION = '0.0.1'

from robot.libraries.BuiltIn import BuiltIn


class Mails:
    def __init__(self):
        self.sel = BuiltIn().get_library_instance('Selenium2Library')
        self.host = "127.0.0.1"
        self.port = "1025"
        self.web = "127.0.0.1:1080"

    def setupSmtp(self, host="127.0.0.1", port="1025"):
        self.host = host
        self.port = port

    def setupWeb(self, web="127.0.0.1:1080"):
        self.web = web

    def configuration(self):
        return "--smtp-ip {} --smtp-port {} --http-ip {} -a".format(self.host,
                                                                    self.port, self.web)

    def find_email(self, recipient):
        self.sel.click_element("xpath=//td[contains(text(),'" + recipient + "')]")

    def get_url(self):
        return "http://{}/".format(self.web)

    def get_random_email(self, partial="test-email"):
        return "{}{}@heliard.ru".format(partial, time.time())

    def get_password(self):
        css_path = "css=table>tbody>tr:nth-child(7)>td:nth-child(7)>p:nth-child(8)"
        el = self.sel._element_find(css_path, True, True, tag='p')
        if el is None:
            raise AssertionError("Cannot receive password")
        return el.text.replace(u'Пароль:','').strip()

    def get_login(self):
        xpath_path = "xpath=//table/tbody/tr[7]/td[7]/p[2]"
        el = self.sel._element_find(xpath_path, True, True, tag='p')
        if el is None:
            raise AssertionError("Cannot receive password")
        return el.text.replace(u'Логин:','').strip()

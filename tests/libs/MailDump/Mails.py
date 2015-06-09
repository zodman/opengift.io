# -*- coding:utf-8 -*-
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

    def email_received(self, to="", frm="", subject="", body="", body_partial=""):
        self.sel.go_to(self.web)

    def get_url(self):
        return "http://{}/".format(self.web)

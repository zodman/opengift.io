__author__ = 'gvammer'
import os

class JSSniffer:
    @staticmethod
    def sniff(filename):
        return os.popen('phpcs ' + filename)
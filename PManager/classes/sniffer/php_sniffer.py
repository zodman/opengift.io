__author__ = 'gvammer'
import os

class PHPSniffer:
    @staticmethod
    def sniff(filename):
        return os.popen('jscs ' + filename + ' --standard=Jquery --report=full')
__author__ = 'gvammer'
import os

class PHPSniffer:
    @staticmethod
    def sniff(filename):
        a = os.popen('phpcs ' + filename)
        i = 0
        ar = []
        for s in a:
            i += 1
            if i < 5:
                continue
            s = s.split('|')
            o = {
                'line': s[0],
                'type': s[1],
                'comment': s[2]
            }
            ar.append(o)

        return ar
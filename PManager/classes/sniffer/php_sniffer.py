__author__ = 'gvammer'
import os

class PHPSniffer:
    @staticmethod
    def sniff(filename):
        a = os.popen('phpcs --standard=PSR2 ' + filename)
        i = 0
        ar = []
        for s in a:
            i += 1
            if i < 5:
                continue

            s = s.split('|')
            if len(s) < 3:
                continue

            ar.append({
                'line': s[0],
                'type': s[1],
                'comment': s[2]
            })

        return ar
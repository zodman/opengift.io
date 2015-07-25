__author__ = 'gvammer'
import os


class JSSniffer:
    @staticmethod
    def sniff(filename):
        a = os.popen('jscs ' + filename + ' --standard=Jquery --report-full')
        i = 0
        ar = []
        for s in a:
            i += 1
            if i < 10:
                continue
            s = s.split('|')
            if len(s) < 3:
                continue
            ar.append({
                'line': s[0],
                'type': s[2].split(':')[0],
                'comment': s[2].split(':')[1]
            })

        return ar
__author__ = 'gvammer'
import os


class JSSniffer:
    def __init__(self):
        pass

    @staticmethod
    def sniff(filename):
        # todo: reportWidth must be longer than longest of error messages
        # todo: parse with arbitrary width - ignore newlines
        # highlight==0  to remove console chars colors from output
        # 2>&1 - to capture stderr, since report is going there
        sniffer_output = os.popen(
            'jscs ' + filename + ' --standard=Jquery --highlight=0 --reportWidth=1000 --report-full 2>&1')
        report = []
        i = 0
        for line in sniffer_output:
            i += 1
            if i < 10:
                continue
            line = line.split('|')
            if len(line) >= 3:
                _type, comment = line[2].split(':')
                report.append({
                    'line': line[0],
                    'type': _type,
                    'comment': comment
                })
        return report

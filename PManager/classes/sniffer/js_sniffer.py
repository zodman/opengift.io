__author__ = 'gvammer'
import os
from tracker.settings import PROJECT_ROOT


class JSSniffer:
    def __init__(self):
        pass

    @staticmethod
    def sniff(filename):
        command = 'jscs ' + filename + ' --standard=Jquery --report-full -c ' + JSSniffer.get_config_path()
        print "##########################"
        print command
        print "##########################"

        sniffer_output = os.popen(command)

        for i in sniffer_output:
            print i
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

    @staticmethod
    def get_config_path():
        return os.path.join(PROJECT_ROOT, 'tracker/sniffer_files/jscs-config.json')

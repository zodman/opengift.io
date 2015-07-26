import re
import os


class FileDiff(object):
    ACTION_DELETE = "D"
    ACTION_MODIFY = "M"
    ACTION_CREATE = "C"

    def __init__(self, diff):
        self.summary = {'binary': False, 'deleted': 0, 'created': 0}
        self.raw_lines = []
        self.lines = []
        self.action = self.ACTION_MODIFY
        self.path = ''
        self.error_qty = []
        for line in diff:
            self.parse_line(line)
        self.diff = "\n".join(self.raw_lines)
        self.analyse_lines()

    def parse_line(self, line):
        if line.startswith('deleted file mode'):
            self.action = self.ACTION_DELETE
            return
        if line.startswith('new file mode'):
            self.action = self.ACTION_CREATE
            return
        if line.startswith('Binary files'):
            self.summary['binary'] = True
            self.add_binary_to_summary()
            return
        if line.startswith('diff --git'):
            self.parse_file_name(line)
            return
        if line.startswith('index'):
            return
        if line.startswith('+++') or line.startswith('---'):
            return
        if line.startswith('+'):
            self.summary['created'] += 1
        if line.startswith('-'):
            self.summary['deleted'] += 1
        self.raw_lines.append(line)

    def add_binary_to_summary(self):
        if self.action == FileDiff.ACTION_CREATE:
            self.summary['created'] += 1
        elif self.action == FileDiff.ACTION_DELETE:
            self.summary['deleted'] += 1

    def parse_file_name(self, line):
        pattern = re.compile(r'^diff --git a/(?P<file_name>.*) b/\1$')
        m = pattern.match(line)
        if m:
            file_name = m.group('file_name')
            self.path = os.path.join('/', file_name)

    def analyse_lines(self):
        if len(self.raw_lines) == 0:
            return

        old_number, new_number, line = self.analyse_summary()
        if len(line) > 1:
            self.raw_lines[0] = line
        for text in self.raw_lines[1:]:
            if text.startswith("\ No newline"):
                continue
            line = self.extract_line_metadata(new_number, old_number, text)
            self.lines.append(line)

    @staticmethod
    def extract_line_metadata(new_number, old_number, text):
        line = {
            'same': False,
            'deleted': False,
            'created': False,
            'old_number': old_number,
            'new_number': new_number,
            'text': text
        }
        if text.startswith('-'):
            line['deleted'] = True
            line['new_number'] = ""
            old_number += 1
        elif text.startswith('+'):
            line['created'] = True
            line['old_number'] = ""
            new_number += 1
        else:
            line['same'] = True
            old_number += 1
            new_number += 1
        return line

    def analyse_summary(self):
        line = self.raw_lines[0]
        line_data = line.split("@@")
        if len(line_data) < 3:
            raise Exception("Bad starting diff string")
        line = line_data[2]
        numbers_data = line_data[1].lstrip().rstrip().split(" ")
        try:
            ln = int(numbers_data[1][1::].split(",")[0])
            lo = int(numbers_data[0][1::].split(",")[0])
        except ValueError:
            ln = 0
            lo = 0
        return ln, lo, line

# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
import re, os


class DiffParser(object):
    DELETED_LINE_START = "-"
    CREATED_LINE_START = "+"
    _raw = None
    _raw_length = 0
    message_end_offset = 0
    _hash = None
    _author = None
    _date = None
    _message = None
    _files = None

    def __init__(self, raw):
        if raw is None or len(raw) <= 0:
            raise IOError("Cannot parse empty diff")
        if not raw.startswith("commit"):
            raise IOError("Cannot parse unparsable diff")
        self.parse(raw)

    def raw(self, line):
        if self._raw_length <= line:
            return ''
        return self._raw[line]

    def parse(self, raw):
        """
        Function load data from raw git diff to a object
        :param raw: git diff output
        :return: Nothing
        """
        self._raw = raw.split('\n')
        self._raw_length = len(self._raw)
        self.__load_message()
        self.__load_author()
        self.__load_date()
        self.__load_hash()
        self.__load_files()

    @staticmethod
    def __parse_binary(file_obj, m):
        mode = False
        (old_path, new_path) = m.groups()
        if old_path == '/dev/null':
            mode = "C"
            file_obj['path'] = new_path
        elif new_path == '/dev/null':
            mode = "D"
            file_obj['path'] = old_path
        else:
            file_obj['path'] = new_path
        file_obj['action'] = mode
        file_obj['diff'] = False
        file_obj['lines'] = []
        file_obj['summary'] = {
            "deleted": 1 if mode == "D" else 0,
            "created": 1 if mode == "C" else 0,
            "binary": True
        }
        return file_obj

    @staticmethod
    def __get_lines(diff):
        df = diff.lstrip().rstrip().split('\n')
        lines = []
        line = None
        (ln, lo) = (0, 0)
        for diff_line in df:
            if diff_line.startswith("@@"):
                (ln, lo, diff_line) = DiffParser.__get_start_line_numbers(diff_line)
                if len(diff_line) < 1:
                    continue
                if line:
                    line['end'] = True
            line = {'same': False, 'deleted': False, 'created': False, 'old_number': lo, 'new_number': ln,
                    'end': False}
            if diff_line.startswith("\ No newline"):
                continue
            if diff_line.startswith(DiffParser.DELETED_LINE_START):
                line['deleted'] = True
                line['new_number'] = ""
                lo += 1
            elif diff_line.startswith(DiffParser.CREATED_LINE_START):
                line['created'] = True
                line['old_number'] = ""
                ln += 1
            else:
                line['same'] = True
                ln += 1
                lo += 1
            line['text'] = diff_line
            lines.append(line)
        return lines

    @staticmethod
    def __get_start_line_numbers(line):
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

    @staticmethod
    def __get_line_count(symbol, lines):
        count = 0
        for diff_line in lines:
            if diff_line[symbol]:
                count += 1
        return count

    @property
    def hash(self):
        return self._hash

    @property
    def author(self):
        return self._author

    @property
    def commit_message(self):
        return self._message

    @property
    def date(self):
        return self._date

    @property
    def message(self):
        return self._message

    @property
    def files(self):
        if not self._files:
            self.__load_files()
        return self._files

    def __load_hash(self):
        self._hash = self.raw(0).replace("commit ", "")

    def __load_author(self):
        data = self.raw(1).replace("Author: ", "")
        ts = data.split("<")
        self._author = {"name": ts[0].strip(" "), "email": ts[1].strip(" ><")}

    def __load_date(self):
        data = self.raw(2).replace("Date: ", "").strip(" ")
        self._date = data

    def __load_message(self):
        message_ends = False
        data = ""
        i = 3
        while not message_ends:
            data += self.raw(i).strip(" \t") + "\n"
            i += 1
            if re.search('diff --git', self.raw(i)):
                message_ends = True
                self.message_end_offset = i
        self._message = data.strip(" \n\r")

    def __load_files(self):
        files = []
        for i in range(self.message_end_offset, len(self._raw)):
            if self.raw(i).startswith("diff --git"):
                files.append(self.__parse_file_str(i))
        self._files = files

    def __get_file_name(self, start):
        pattern = re.compile(r'^diff --git a/(?P<file_name>.*) b/\1$')
        m = pattern.match(self.raw(start))
        if m:
            file_name = m.group('file_name')
            return os.path.join('/', file_name)

    def __parse_file_str(self, start):
        file_obj = dict()
        file_str = self.__get_file_name(start)
        next_string = self.raw(start + 1)
        mode = "M"
        diff_start = start
        if self.raw(start + 3).startswith("Binary files"):
            pattern = re.compile('Binary files "?a?(?P<old_path>[A-zА-я0-9_\/. -]+)"?' +
                                 ' and "?b?(?P<new_path>[A-zА-я0-9_\/. -]+)"? differ')
            m = pattern.search(self.raw(start + 3))
            if m:
                return self.__parse_binary(file_obj, m)
        if next_string.startswith("deleted file mode"):
            diff_start = start + 5
            mode = "D"
        elif next_string.startswith("new file mode"):
            diff_start = start + 5
            mode = "C"
        elif next_string.startswith("index"):
            diff_start = start + 4
        file_obj['path'] = file_str
        file_obj['action'] = mode
        file_obj['diff'] = self.__get_file_diff(diff_start)
        file_obj['lines'] = self.__get_lines(file_obj['diff'])
        file_obj['summary'] = {
            "deleted": self.__get_line_count('deleted', file_obj['lines']),
            "created": self.__get_line_count('created', file_obj['lines']),
            "binary": False
        }
        return file_obj

    def __get_file_diff(self, start):
        diff = ""
        i = start
        end = len(self._raw)
        if i > end:
            return diff
        while i < end and not self.raw(i).startswith("diff --git"):
            diff += self.raw(i) + "\n"
            i += 1
        return diff

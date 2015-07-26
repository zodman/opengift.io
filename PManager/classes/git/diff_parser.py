# -*- coding:utf-8 -*-
__author__ = 'Tonakai'
import re

from PManager.classes.git.file_diff import FileDiff


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
        self._files = self.__parse_files(self.message_end_offset)

    def __get_files_diff(self, start):
        files = []
        _file = []
        for i in range(start, self._raw_length):
            if self.raw(i).startswith('diff --git') and len(_file) > 0:
                files.append(_file)
                _file = [self.raw(i)]
            else:
                _file.append(self.raw(i))
        if len(_file) > 0:
            files.append(_file)
        return files

    def __parse_files(self, start):
        files = self.__get_files_diff(start)
        files_parsed = []
        for f in files:
            files_parsed.append(FileDiff(f))
        return files_parsed




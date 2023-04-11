from abc import ABC, abstractmethod


def line_without_comment_part(line):
    return line.split('#')[0]


class Rule(ABC):

    def __init__(self, code, msg, file):
        self.MSG_TPL = '%s: Line %d: %s %s'
        self.CODE = code
        self.MSG = msg
        self.count = 0
        self.file = file

    @abstractmethod
    def is_ok(self, line, line_no=None):
        pass

    def message(self, file_path, line_no):
        return self.MSG_TPL % (
            file_path,
            line_no, self.code(), self.MSG)

    def has_failed(self, line, line_no=None):
        return not self.is_ok(line, line_no)

    def code(self):
        return self.CODE

    def count_condition(self, line):
        return self

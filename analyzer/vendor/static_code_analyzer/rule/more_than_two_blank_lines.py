from .rule import Rule
from .rule_definition import S006_MSG
from .rule_definition import S006_CODE

MAX_BLANK_LINES = 3


def line_ok(line):
    return len(line.strip()) != 0


class MoreThanTwoBlankLines(Rule):

    def __init__(self, file):
        self.isok = True
        super().__init__(S006_CODE, S006_MSG, file)

    def is_ok(self, line, line_no=None):
        return self.isok

    def has_failed(self, line, line_no=None):
        has_failed = not self.is_ok(line)

        #erase state
        if has_failed:
            self.isok = True
            self.count = 0

        return has_failed

    def count_condition(self, line):

        if line_ok(line):
            self.isok = self.condition_ok()
            self.count = 0

        if not line_ok(line):
            self.count += 1

        return self

    def condition_ok(self):
        return self.count < MAX_BLANK_LINES

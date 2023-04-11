from .rule import Rule
from .rule_definition import S002_MSG
from .rule_definition import S002_CODE

LINE_MAX_LENGTH = 79


class Indentation(Rule):

    def __init__(self, file):
        super().__init__(S002_CODE, S002_MSG, file)

    def is_ok(self, line, line_no=None):
        return len(line.lstrip()) == 0 or (len(line) - len(line.lstrip())) % 4 == 0

    def count_condition(self, line):
        if len(line.strip()) == 0:
            self.count += 1
        return self

import re

from .rule import Rule
from .rule_definition import S009_CODE
from .rule_definition import S009_MSG

LINE_MAX_LENGTH = 79


class FunctionNameShouldBeSnakeCase(Rule):

    def __init__(self, file):
        super().__init__(S009_CODE, S009_MSG, file)

    def is_ok(self, line, line_no=None):
        return ('def' not in line) or re.match(r'.*def\s+[_a-z]+(_[_a-z]+)*.*', line)

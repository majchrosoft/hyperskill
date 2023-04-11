from .rule import Rule
from .rule_definition import S007_MSG
from .rule_definition import S007_CODE
import re

LINE_MAX_LENGTH = 79


class TooManySpaces(Rule):

    def __init__(self, file):
        super().__init__(S007_CODE, S007_MSG, file)

    def is_ok(self, line, line_no=None):
        # (not re.match(r'\s{2,}(class|def)', line)) and
        return not re.match(r'\s*(class|def)\s{2,}', line)

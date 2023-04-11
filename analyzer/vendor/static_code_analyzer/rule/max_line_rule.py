from .rule import Rule
from .rule_definition import S001_MSG
from .rule_definition import S001_CODE

LINE_MAX_LENGTH = 79


class MaxLineRule(Rule):

    def __init__(self, file):
        super().__init__(S001_CODE, S001_MSG, file)

    def is_ok(self, line, line_no=None):
        return len(line) <= LINE_MAX_LENGTH

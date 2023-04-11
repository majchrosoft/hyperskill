from .rule import Rule
from .rule_definition import S004_MSG
from .rule_definition import S004_CODE

LINE_MAX_LENGTH = 79


class TwoSpacesBeforeComment(Rule):

    def __init__(self, file):
        super().__init__(S004_CODE, S004_MSG, file)

    def is_ok(self, line, line_no=None):
        return \
                '#' not in line \
                or len(line.split('#')[0]) == 0 \
                or (len(line.split('#')[0]) - len(line.split('#')[0].rstrip()) > 1)

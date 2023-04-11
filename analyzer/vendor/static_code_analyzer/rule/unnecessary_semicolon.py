from .rule import Rule
from .rule_definition import S003_MSG
from .rule_definition import S003_CODE
from .rule import line_without_comment_part

LINE_MAX_LENGTH = 79


class UnnecessarySemicolon(Rule):

    def __init__(self, file):
        super().__init__(S003_CODE, S003_MSG, file)

    def is_ok(self, line, line_no=None):
        return not line_without_comment_part(line).strip().endswith(';')
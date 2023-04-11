from .rule import Rule
from .rule_definition import S005_MSG
from .rule_definition import S005_CODE

LINE_MAX_LENGTH = 79


class TodoFound(Rule):

    def __init__(self, file):
        super().__init__(S005_CODE, S005_MSG, file)

    def is_ok(self, line, line_no=None):
        line_exploded = line.split('#', maxsplit=1)
        comment = line_exploded[1] if len(line_exploded) > 1 else ''
        return 'todo' not in comment.lower()

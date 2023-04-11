import re

from .rule import Rule
from .rule_definition import S008_CODE
from .rule_definition import S008_MSG

LINE_MAX_LENGTH = 79


class ClassNameShouldCamelCase(Rule):

    def __init__(self, file):
        super().__init__(S008_CODE, S008_MSG, file)

    def is_ok(self, line, line_no=None):
        return ('class' not in line) or bool(re.match(r'class\s+(?=[A-Z])[A-Za-z\d]*([A-Z][A-Za-z\d]*)*(:|\()', line))

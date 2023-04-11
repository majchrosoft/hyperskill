import ast
import re

from .rule import Rule
from .rule_definition import S010_CODE
from .rule_definition import S010_MSG

LINE_MAX_LENGTH = 79


def is_snake_case(s):
    return bool(re.match(r'^[a-z]+(_[a-z]+)*$', s))


class NotSnakeCaseArgumentLister(ast.NodeVisitor):

    def __init__(self, rule):
        self.rule = rule
        super().__init__()

    def visit_FunctionDef(self, node):
        for arg in node.args.args:
            # ignore if is snake case
            if is_snake_case(arg.arg):
                continue
            # set predefined empty value in dict
            if arg.lineno not in self.rule.invalid_arg_names:
                self.rule.invalid_arg_names[arg.lineno] = []

            # produce message
            msg = self.rule.MSG % arg.arg
            if msg in self.rule.invalid_arg_names[arg.lineno]:
                continue

            # append message
            self.rule.invalid_arg_names[arg.lineno].append(msg)

        self.generic_visit(node)


class ArgNameShouldBeSnakeCase(Rule):

    def __init__(self, file):
        super().__init__(S010_CODE, S010_MSG, file)
        self.invalid_arg_names = {}
        self.setup_arg_name_stats()

    def is_ok(self, line, line_no=None):
        if line_no not in self.invalid_arg_names:
            return True

        return False

    def message(self, file_path, line_no):
        if line_no not in self.invalid_arg_names:
            return ''
        return "\n".join([self.MSG_TPL % (
            file_path,
            line_no, self.code(), msg) for msg in self.invalid_arg_names[line_no]])

    def setup_arg_name_stats(self):
        tree = ast.parse(self.file.read())
        NotSnakeCaseArgumentLister(self).visit(tree)

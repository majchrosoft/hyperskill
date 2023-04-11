import re
import ast
from .rule import Rule
from .rule_definition import S011_CODE
from .rule_definition import S011_MSG

LINE_MAX_LENGTH = 79


def is_snake_case(s):
    return bool(re.match(r'^[a-z]+(_[a-z]+)*$', s))


class NotSnakeCaseVariableLister(ast.NodeVisitor):

    def __init__(self, rule):
        self.rule = rule
        super().__init__()

    def visit_Assign(self, node):

        target_name = lambda node_arg: node_arg.targets[0].id

        if not isinstance(node.targets[0], ast.Name) or is_snake_case(target_name(node)):
            self.generic_visit(node)
            return

        # set predefined empty value in dict
        if node.lineno not in self.rule.invalid_arg_names:
            self.rule.invalid_arg_names[node.lineno] = []

        # produce message
        msg = self.rule.MSG % target_name(node)
        # append message
        if msg not in self.rule.invalid_arg_names[node.lineno]:
            self.rule.invalid_arg_names[node.lineno].append(msg)
        self.generic_visit(node)


class VarNameShouldBeSnakeCase(Rule):

    def __init__(self, file):
        super().__init__(S011_CODE, S011_MSG, file)
        self.invalid_arg_names = {}
        self.setup_var_name_stats()

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

    def setup_var_name_stats(self):
        tree = ast.parse(self.file.read())
        NotSnakeCaseVariableLister(self).visit(tree)

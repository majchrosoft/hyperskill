import re
import ast
from .rule import Rule
from .rule_definition import S012_CODE
from .rule_definition import S012_MSG

LINE_MAX_LENGTH = 79


def is_snake_case(s):
    return bool(re.match(r'^[a-z]+(_[a-z]+)*$', s))


class DefaultValueIsMutableLister(ast.NodeVisitor):

    def __init__(self, rule):
        self.rule = rule
        super().__init__()

    def visit_FunctionDef(self, node):
        for arg in node.args.defaults:
            if isinstance(arg, ast.List) or isinstance(arg, ast.Dict):
                # set predefined empty value in dict
                if node.lineno not in self.rule.invalid_arg_names:
                    self.rule.invalid_arg_names[node.lineno] = []

                # produce message
                msg = self.rule.MSG
                # append message
                if msg not in self.rule.invalid_arg_names[node.lineno]:
                    self.rule.invalid_arg_names[node.lineno].append(msg)
                self.generic_visit(node)
                break
        self.generic_visit(node)


class DefaultValueIsMutable(Rule):

    def __init__(self, file):
        super().__init__(S012_CODE, S012_MSG, file)
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
        DefaultValueIsMutableLister(self).visit(tree)

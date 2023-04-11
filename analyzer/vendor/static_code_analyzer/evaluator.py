import copy
import os
from .rule.class_name_should_camel_case import ClassNameShouldCamelCase
from .rule.function_name_should_be_snake_case import FunctionNameShouldBeSnakeCase
from .rule.indentation import Indentation
from .rule.max_line_rule import MaxLineRule
from .rule.more_than_two_blank_lines import MoreThanTwoBlankLines
from .rule.todo_found import TodoFound
from .rule.too_many_spaces import TooManySpaces
from .rule.two_spaces_before_comment import TwoSpacesBeforeComment
from .rule.unnecessary_semicolon import UnnecessarySemicolon
from .rule.arg_name_should_be_snake_case import ArgNameShouldBeSnakeCase
from .rule.var_name_should_be_snake_case import VarNameShouldBeSnakeCase
from .rule.default_value_is_mutable import DefaultValueIsMutable

from .rule.rule_list import RULE_LIST


def list_files(startpath):
    return sorted([os.path.join(root, filename)
                   for root, _, files in os.walk(startpath)
                   for filename in files
                   if os.path.isfile(os.path.join(root, filename))])


def call_rule(file_path, class_name):
    with open(file_path, 'r') as f2:
        return globals()[class_name](f2)


def evaluator_yield(directory_or_file_arg):
    if os.path.isdir(directory_or_file_arg):
        files = list_files(directory_or_file_arg)
    else:
        files = [directory_or_file_arg]

    for file_path in files:

        # @todo uncomment when done
        file_name = os.path.basename(file_path)
        if not file_name.startswith('test_'):
            continue

        with open(file_path, 'r') as f:
            # instantiate the class
            rules = [
                call_rule(file_path, class_name) for class_name in RULE_LIST
            ]

            line_no = 0
            line = f.readline()
            while line:
                line_no += 1
                # print(rules)
                # print([rule.message(file_path, line_no) for rule in rules if
                #        rule.count_condition(line).has_failed(line, line_no)])

                yield [rule.message(file_path, line_no) for rule in rules if
                       rule.count_condition(line).has_failed(line, line_no)]
                line = f.readline()

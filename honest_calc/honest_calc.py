class GoToStartException(Exception):
    pass


class End(Exception):
    pass


MSG_ENTER_EQUATION = "Enter an equation"
MSG_INVALID_FACTOR = "Do you even know what numbers are? Stay focused!"
MSG_INVALID_OPERATOR = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"
MSG_DIVISION_BY_ZERO = "Yeah... division by zero. Smart move..."
MSG_WANT_TO_STORE_RESULT = "Do you want to store the result? (y / n):"
MSG_CONTINUE_CALCULATIONS = "Do you want to continue calculations? (y / n):"
MSG_LAZY = " ... lazy"
MSG_VERY_LAZY = " ... very lazy"
MSG_VERY_VERY_LAZY = " ... very, very lazy"
MSG_YOU_ARE = "You are"

MSG_ARE_YOU_SURE_TO_STORE_RESULT_LIST = [
    "Are you sure? It is only one digit! (y / n)",
    "Don't be silly! It's just one number! Add to the memory? (y / n)",
    "Last chance! Do you really want to embarrass yourself? (y / n)"
]

OPERATOR_NAMES = [
    '+', '-', '*', '/'
]

OPERATOR_DEFINITIONS = [
    lambda x, y: x + y,
    lambda x, y: x - y,
    lambda x, y: x * y,
    lambda x, y: x / y,
]

LAZY_OPERATION_MESSAGES = [
    MSG_LAZY,
    MSG_VERY_LAZY,
    MSG_VERY_VERY_LAZY
]

LAZY_OPERATION_DEFINITIONS = [
    lambda x, y, o: is_one_digit(x) and is_one_digit(y),
    lambda x, y, o: (x == 1 or y == 1) and o == '*',
    lambda x, y, o: (x == 0 or y == 0) and (o == '*' or o == '+' or o == '-'),
]


def is_answer_yes(question):
    while True:
        print(question)
        answer = str(input())
        if answer in ['y', 'n']:
            break
    return answer == 'y'


def is_answer_no(question):
    return not is_answer_yes(question)


def is_one_digit(x_arg):
    return x_arg.is_integer() and 10 > x_arg >= 0


def get_operator(operator):
    operator = str(operator)
    if operator not in OPERATOR_NAMES:
        print(MSG_INVALID_OPERATOR)
        raise GoToStartException
    return operator


def get_factor(factor_arg):
    global memory
    if factor_arg == 'M':
        return memory
    try:
        return float(factor_arg)
    except ValueError:
        print(MSG_INVALID_FACTOR)
        raise GoToStartException


def ask_many_times_yes():
    for are_you_sure_msg in MSG_ARE_YOU_SURE_TO_STORE_RESULT_LIST:
        if is_answer_no(are_you_sure_msg):
            return False
    return True


def ask_should_store_result(result_arg):
    global memory, MSG_ARE_YOU_SURE_TO_STORE_RESULT_LIST, MSG_WANT_TO_STORE_RESULT

    if is_answer_no(MSG_WANT_TO_STORE_RESULT):
        return

    if is_one_digit(result_arg) and not ask_many_times_yes():
        return

    memory = result_arg
    return


def ask_should_continue_calculations():
    if is_answer_yes(MSG_CONTINUE_CALCULATIONS):
        raise GoToStartException
    raise End


def calculate(x_arg, y_arg, op_arg):
    global OPERATOR_DEFINITIONS, OPERATOR_NAMES
    try:
        return OPERATOR_DEFINITIONS[OPERATOR_NAMES.index(op_arg)](x_arg, y_arg)
    except ZeroDivisionError:
        print(MSG_DIVISION_BY_ZERO)
        raise GoToStartException


def show_lazy_message(x_arg, y_arg, op_arg):
    global LAZY_OPERATION_DEFINITIONS, LAZY_OPERATION_MESSAGES, MSG_YOU_ARE
    lazy_parts = [
        LAZY_OPERATION_MESSAGES[index]
        if is_lazy(x_arg, y_arg, op_arg)
        else
        ''
        for index, is_lazy in enumerate(LAZY_OPERATION_DEFINITIONS)
    ]
    very_lazy_suffix = "".join(lazy_parts)
    print(MSG_YOU_ARE + very_lazy_suffix if very_lazy_suffix != '' else '')


memory = 0.0

while True:
    print(MSG_ENTER_EQUATION)
    a_input, op_input, b_input = input().split()
    try:
        a = get_factor(a_input)
        b = get_factor(b_input)
        op = get_operator(op_input)
        show_lazy_message(a, b, op)
        result = calculate(a, b, op)
        print(result)
        ask_should_store_result(result)
        ask_should_continue_calculations()
    except GoToStartException:
        continue
    except End:
        break

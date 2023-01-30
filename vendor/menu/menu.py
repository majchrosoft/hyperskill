from ..input import question

name = 'Menu'


class ExitFlowException(Exception):
    pass


class GoToMainMenuFlowException(Exception):
    pass


def go_out():
    raise ExitFlowException


def init(actions, msg_arg):
    while True:
        try:
            msg = msg_arg % ', '.join(actions.keys()) if len(msg_arg) > 0 else ''
            actions[question.closed_str(msg, actions.keys())]()
            print()
        except ExitFlowException:
            break
        except GoToMainMenuFlowException:
            continue

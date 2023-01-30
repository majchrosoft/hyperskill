name = 'Question'


def open_question(message_arg, cast_to_arg=int):
    len(message_arg) > 0 and print(message_arg)
    return cast_to_arg(input())


def closed(message_arg, possible_answers_arg, cast_to, message_fail_arg='',
                        message_fail_extended_arg=None):
    while True:
        try:
            message_arg and print(message_arg)

            user_input = input()
            if user_input == 'back':
                raise GoToMainMenuFlowException

            answer = cast_to(user_input)
        except ValueError:
            message_fail_arg and print(message_fail_arg)
            return ask_question_closed(message_arg, possible_answers_arg, cast_to, message_fail_arg,
                                       message_fail_extended_arg)

        if answer in possible_answers_arg:
            break
        message_fail_extended_arg is not None and message_fail_extended_arg(answer, possible_answers_arg)
        message_fail_arg and print(message_fail_arg)
    return answer


def closed_str(message_arg, possible_answers_arg, message_fail_arg='',
                        message_fail_extended_arg=None):
    return closed(message_arg, possible_answers_arg, str, message_fail_arg, message_fail_extended_arg)

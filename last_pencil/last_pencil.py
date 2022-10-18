from random import randint

PLAYERS = ['John', 'Jack']
HOW_MANY_PENCILS_WOULD_YOU_LIKE_TO_USE = 'How many pencils would you like to use:'
WHO_WILL_BE_THE_FIRST = 'Who will be the first (%s):'
MSG_CHOOSE_BETWEEN = 'Choose between %s:'
PLAYER_TURN = '%s\'s turn%s'

THE_NUMBER_OF_PENCILS_SHOULD_BE_NUMERIC = 'The number of pencils should be numeric'
THE_NUMBER_OF_PENCILS_SHOULD_BE_POSITIVE = 'The number of pencils should be positive'
MSG_POSSIBLE_VALUES = 'possible values: %s'
MSG_TOO_MANY_PENCILS_WERE_TAKEN = 'Too many pencils were taken'
MSG_PLAYER_WON = '%s won!'

POSSIBLE_VALUES = [1, 2, 3]


def calculate_is_winning_position(pencils_arg):
    return pencils_arg % 4 != 1


def bot_choose(pencils_arg):
    the_rest = 1
    if pencils_arg % 4 == 0:
        the_rest = 3
    elif pencils_arg % 4 in [2, 3]:
        the_rest = pencils_arg % 4 - 1

    choose = the_rest if calculate_is_winning_position(pencils_arg) else randint(1, pencils_arg % 4)
    print(choose)
    return choose


def ask_question_closed(message_arg, possible_answers_arg, cast_to, message_fail_arg='',
                        message_fail_extended_arg=None):
    while True:
        try:
            message_arg and print(message_arg)
            answer = cast_to(input())
        except ValueError:
            message_fail_arg and print(message_fail_arg)
            return ask_question_closed(message_arg, possible_answers_arg, cast_to, message_fail_arg,
                                       message_fail_extended_arg)

        if answer in possible_answers_arg:
            break
        message_fail_extended_arg is not None and message_fail_extended_arg(answer, possible_answers_arg)
        message_fail_arg and print(message_fail_arg)
    return answer


def ask_question_open(message_arg):
    print(message_arg)
    return input()


def ask_question_open_int(message_arg):
    while True:
        try:
            message_arg and print(message_arg)
            return int(input())
        except ValueError:
            print(THE_NUMBER_OF_PENCILS_SHOULD_BE_NUMERIC)


def ask_question_open_positive_int(message_arg):
    answer = ask_question_open_int(message_arg)

    return (answer if answer > 0 else (
            print(THE_NUMBER_OF_PENCILS_SHOULD_BE_POSITIVE)
            or ask_question_open_positive_int(message_arg)))


def calculate_player_next_index(player_current_index_arg, players_arg):
    return (player_current_index_arg + 1) % len(players_arg)


def message_fail_extended(value, possible_values):
    if type(value) != int or value in possible_values:
        return
    return print(MSG_TOO_MANY_PENCILS_WERE_TAKEN)


def main():
    print(HOW_MANY_PENCILS_WOULD_YOU_LIKE_TO_USE)
    pencils_nr = ask_question_open_positive_int('')
    players_str = ', '.join(PLAYERS)
    player_current_index = PLAYERS.index(
        ask_question_closed(WHO_WILL_BE_THE_FIRST % players_str, PLAYERS, str, (MSG_CHOOSE_BETWEEN % players_str)))

    print('|' * pencils_nr)

    player_index = 0

    while pencils_nr > 0:
        possible_values_left = [possible_value for possible_value in POSSIBLE_VALUES if possible_value <= pencils_nr]
        possible_values_left_str = ["%d" % possible_value for possible_value in possible_values_left]
        msg_player_turn = PLAYER_TURN % (
            PLAYERS[player_current_index], '!' if player_index == player_current_index else ':'
        )
        # print(msg_player_turn)
        pencils_nr -= ask_question_closed(
            # '',
            msg_player_turn,
            possible_values_left,
            int,
            MSG_POSSIBLE_VALUES % POSSIBLE_VALUES,
            # MSG_POSSIBLE_VALUES % possible_values_left,
            # MSG_POSSIBLE_VALUES % ', '.join(possible_values_left_str),
            message_fail_extended
        ) if player_current_index == player_index else (print(msg_player_turn) or bot_choose(pencils_nr))

        pencils_nr and print('|' * pencils_nr)
        player_current_index = calculate_player_next_index(player_current_index, PLAYERS)

    print(MSG_PLAYER_WON % PLAYERS[player_current_index])


if __name__ == "__main__":
    main()

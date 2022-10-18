from random import choice


class ExitFlowException(Exception):
    pass


MSG_YOU_SURVIVED = 'You survived!'
MSG_YOU_LOST = 'You lost!'
MSG_THANK_YOU_FOR_PLAYING = 'Thanks for playing!'
MSG_HANGMAN = 'H A N G M A N'
MSG_INPUT_A_LETTER = 'Input a letter:'
MSG_THAT_LETTER_DOESNT_APPEAR_IN_THE_WORD = "That letter doesn't appear in the word."
MSG_NO_IMPROVEMENTS = 'No improvements.'
MSG_YOU_GUESSED_THE_WORD = 'You guessed the word %s!'
MSG_PLEASE_INPUT_A_SINGLE_LETTER = 'Please, input a single letter'
MSG_PLEASE_ENTER_A_VALID_LETTER = 'Please, enter a lowercase letter from the English alphabet.'
MSG_YOU_ALREADY_GUESSED_THIS_LETTER = "You've already guessed this letter"
MSG_MENU = 'Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit:'
MSG_YOU_WON_TIMES = 'You won: %d times.'
MSG_YOU_LOST_TIMES = 'You lost: %d times.'

OPTION_PYTHON = 'python'
OPTION_JAVA = 'java'
OPTION_SWIFT = 'swift'
OPTION_JAVASCRIPT = 'javascript'

MASK_SIGN = '-'
ATTEMPTS = 8

OPTIONS_POSSIBLE = OPTION_PYTHON, OPTION_JAVA, OPTION_SWIFT, OPTION_JAVASCRIPT,

MENU_OPTION_PLAY = 'play'
MENU_OPTION_RESULTS = 'results'
MENU_OPTION_EXIT = 'exit'

MENU_OPTIONS = MENU_OPTION_PLAY, MENU_OPTION_RESULTS, MENU_OPTION_EXIT


def question_closed(question, answers_possible):
    while True:
        print(question)
        answer = str(input())
        if answer in answers_possible:
            break
    return answer


def list_to_str(list_arg):
    return ''.join(list_arg)


def is_puzzle_resolved(guess_arg, option_valid):
    return list_to_str(guess_arg) == option_valid


def input_char(msg_err):
    while True:
        try:
            inp = str(input())
            if len(inp) != 1:
                print(MSG_PLEASE_INPUT_A_SINGLE_LETTER)
                print()
                print(msg_err)
                print(MSG_INPUT_A_LETTER)
                continue
            if not inp.isalpha() or not inp.islower():
                print(MSG_PLEASE_ENTER_A_VALID_LETTER)
                print()
                print(msg_err)
                print(MSG_INPUT_A_LETTER)
                continue
            return inp
        except ValueError:
            pass


def raise_exit_flow_exception():
    raise ExitFlowException


wins = 0
loses = 0


def increase_wins():
    global wins
    wins += 1
    return True


def increase_loses():
    global loses
    loses += 1
    return True


def show_results():
    global wins, loses
    print(MSG_YOU_WON_TIMES % wins)
    print(MSG_YOU_LOST_TIMES % loses)


def play():
    option_valid = choice(OPTIONS_POSSIBLE)
    guess = MASK_SIGN * len(option_valid)
    attempts_left = ATTEMPTS
    resolved = False
    guess_chars = set()
    while attempts_left > 0 and not resolved:
        print(list_to_str(guess))
        print(MSG_INPUT_A_LETTER)
        guess_char = input_char(list_to_str(guess))

        if guess_char in guess_chars:
            print(MSG_YOU_ALREADY_GUESSED_THIS_LETTER)
            continue
        if guess_char not in option_valid:
            attempts_left -= 1
            print(MSG_THAT_LETTER_DOESNT_APPEAR_IN_THE_WORD)
            guess_chars.add(guess_char)
            continue

        guess_chars.add(guess_char)
        guess = [char if guess[ind] != MASK_SIGN or guess_char == char else MASK_SIGN for ind, char in
                 enumerate(option_valid)]
        resolved = is_puzzle_resolved(guess, option_valid)

    not resolved and increase_loses() and print(MSG_YOU_LOST)
    resolved and increase_wins() and print(MSG_YOU_GUESSED_THE_WORD % option_valid)
    resolved and print(MSG_YOU_SURVIVED)


MENU_RESOLVERS = {
    MENU_OPTION_PLAY: play,
    MENU_OPTION_EXIT: raise_exit_flow_exception,
    MENU_OPTION_RESULTS: show_results
}


def main():
    print(MSG_HANGMAN)
    print()
    while True:
        try:
            MENU_RESOLVERS[question_closed(MSG_MENU, MENU_OPTIONS)]()
        except ExitFlowException:
            break


if __name__ == '__main__':
    main()
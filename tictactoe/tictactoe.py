class ValidatorException(Exception):
    pass


# write your code here
X = 'X'
O = 'O'
_ = ' '

EXAMPLE_FIELD = [
    [X, O, X, ],
    [O, X, O, ],
    [X, X, O, ],
]

MSG_GAME_STATES_GAME_NOT_FINISHED = "Game not finished"  # when neither side has three in a row but the grid still has empty cells.
MSG_GAME_STATES_DRAW = "Draw"  # when no side has a three in a row and the grid has no empty cells.
MSG_GAME_STATES_X_WINS = "X wins"  # when the grid has three X's in a row (including diagonals).
MSG_GAME_STATES_O_WINS = "O wins"  # when the grid has three O's in a row (including diagonals).
MSG_GAME_STATES_IMPOSSIBLE = "Impossible"

MSG_THIS_CELL_IS_OCCUPIED_CHOOSE_ANOTHER_ONE = 'This cell is occupied! Choose another one!'
MSG_YOU_SHOULD_ENTER_NUMBERS = 'You should enter numbers!'
MSG_COORDINATES_SHOULD_BE_FROM_1_TO_3 = 'Coordinates should be from 1 to 3!'

MSG_PLAYER_WINS = '%s wins'


def next_set(move_by, the_set):
    return [ind + move_by for ind in the_set]


def has_three_in_a_row(pattern, player_sign):
    won_str = player_sign * 3
    first_column = [0, 3, 6]
    first_row = [0, 1, 2]

    win_positions = [
        first_column,
        next_set(1, first_column),
        next_set(2, first_column),
        first_row,
        next_set(3, first_row),
        next_set(6, first_row),
        [0, 4, 8],
        [2, 4, 6]
    ]
    for win_position in win_positions:
        has_won = (won_str == ''.join([pattern[position] for position in win_position]))
        if has_won:
            return True
    return False


def has_empty_cells(pattern):
    return _ in pattern


GAME_STATE_RESOLVERS = {
    MSG_GAME_STATES_IMPOSSIBLE: lambda x_won, o_won, free_cells, pattern: (x_won and o_won) or abs(
        pattern.count(O) - pattern.count(X)) > 1,
    MSG_GAME_STATES_X_WINS: lambda x_won, o_won, free_cells, pattern: x_won,
    MSG_GAME_STATES_O_WINS: lambda x_won, o_won, free_cells, pattern: o_won,
    MSG_GAME_STATES_GAME_NOT_FINISHED: lambda x_won, o_won, free_cells, pattern: not x_won and not o_won and free_cells,
    MSG_GAME_STATES_DRAW: lambda x_won, o_won, free_cells, pattern: not x_won and not o_won and not free_cells,
}

MATRIX_DIM = 3
POSSIBLE_VALUES = [X, O, _]
PLAYERS = [X, O]
MSG_POSSIBLE_VALUES = 'Possible values: %s'


def print_line_horizontal(matrix_arg):
    print('-' * pow(len(matrix_arg[0]), 2))


def board_print(matrix_arg):
    print_line_horizontal(matrix_arg)
    for row in matrix_arg:
        print('| ' + (' '.join(row)) + ' |')
    print_line_horizontal(matrix_arg)


def board_empty(dim_arg):
    return [[''] * dim_arg] * dim_arg


def pattern_pick():
    return str(input())


def player_next(player):
    return PLAYERS[(PLAYERS.index(player) + 1) % len(PLAYERS)]


def coords_pick(board_arg):
    coords_validators = {
        MSG_COORDINATES_SHOULD_BE_FROM_1_TO_3: lambda x_arg, y_arg, board: (1 <= x_arg <= 3) and (1 <= y_arg <= 3),
        MSG_THIS_CELL_IS_OCCUPIED_CHOOSE_ANOTHER_ONE: lambda x_arg, y_arg, board: board[x_arg - 1][y_arg - 1] == ' ',
    }
    while True:
        inp = str(input())
        if ' ' not in inp:
            print(MSG_YOU_SHOULD_ENTER_NUMBERS)
            continue
        elif not inp.replace(' ', '').isnumeric():
            print(MSG_YOU_SHOULD_ENTER_NUMBERS)
            continue
        # php explode
        inp_list = inp.split(' ')
        x = int(inp_list[0])
        y = int(inp_list[1])
        try:
            for msg in coords_validators:
                if not coords_validators[msg](x, y, board_arg):
                    print(msg)
                    raise ValidatorException
        except ValidatorException:
            continue

        return [x - 1, y - 1]


def pattern_normalize(pattern):
    return pattern.replace('_', _)


def pattern_add_move(pattern, move, player):
    pattern_list = list(pattern)
    pattern_list[(move[0] * MATRIX_DIM) + move[1]] = player
    return ''.join(pattern_list)


def board_from_pattern(pattern, dim_arg):
    return [
        list(row_str)
        for row_str in
        [pattern[i:i + dim_arg] for i in range(0, dim_arg * dim_arg, dim_arg)]
    ]


def step_two():
    board_print(board_from_pattern(coords_pick(), MATRIX_DIM))


def game_state_message(pattern):
    x_won = has_three_in_a_row(pattern, X)
    o_won = has_three_in_a_row(pattern, O)
    free_cells = has_empty_cells(pattern)
    for game_state_msg in GAME_STATE_RESOLVERS:
        if GAME_STATE_RESOLVERS[game_state_msg](x_won, o_won, free_cells, pattern):
            return game_state_msg

    return MSG_GAME_STATES_IMPOSSIBLE


def board_add_move(coords, board, sign):
    board[coords[0]][coords[1]] = sign
    return board


def main():
    pattern = pattern_normalize('_________')
    board = board_from_pattern(pattern, MATRIX_DIM)
    board_print(board)
    current_player = X
    while game_state_message(pattern) == MSG_GAME_STATES_GAME_NOT_FINISHED:
        move = coords_pick(board)
        pattern = pattern_add_move(pattern, move, current_player)
        board = board_add_move(move, board, current_player)
        current_player = player_next(current_player)
        board_print(board)

    print(game_state_message(pattern))


if __name__ == '__main__':
    main()

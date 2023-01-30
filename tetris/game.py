from collections import deque
from copy import deepcopy

import numpy as np

import vendor.input.question as ask
import vendor.menu.menu as menu

MATRIX_DIM = 4
EL_EMPTY = '- '
EL_OCCUPIED = '0 '

COMMAND_ROTATE = 'rotate'
COMMAND_LEFT = 'left'
COMMAND_RIGHT = 'right'
COMMAND_DOWN = 'down'
COMMAND_EXIT = 'exit'

MSG_GAME_OVER = 'Game Over!'

SHAPE_O = 'O'
SHAPE_I = 'I'
SHAPE_S = 'S'
SHAPE_Z = 'Z'
SHAPE_L = 'L'
SHAPE_J = 'J'
SHAPE_T = 'T'

POSITIONS_O = [[4, 14, 15, 5]]
POSITIONS_I = [[4, 14, 24, 34], [3, 4, 5, 6]]
POSITIONS_S = [[5, 4, 14, 13], [4, 14, 15, 25]]
POSITIONS_Z = [[4, 5, 15, 16], [5, 15, 14, 24]]
POSITIONS_L = [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]
POSITIONS_J = [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]
POSITIONS_T = [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]

SHAPE_DIM = 4
SCALAR_LEFT = -1
SCALAR_RIGHT = 1


def make_vector(scalar):
    return np.array([scalar for _ in range(SHAPE_DIM)])


VECTOR_LEFT = make_vector(SCALAR_LEFT)
VECTOR_RIGHT = make_vector(SCALAR_RIGHT)


def vector_down(cols):
    return make_vector(cols)


SHAPE_POSITIONS = {
    SHAPE_O: POSITIONS_O,
    SHAPE_I: POSITIONS_I,
    SHAPE_S: POSITIONS_S,
    SHAPE_Z: POSITIONS_Z,
    SHAPE_L: POSITIONS_L,
    SHAPE_J: POSITIONS_J,
    SHAPE_T: POSITIONS_T,
}


def matrix_to_string(matrix):
    return '\n'.join([''.join(row).rstrip() for row in matrix])


def matrix_make(cols, rows, resolve_value):
    return np.array([[resolve_value(row, col) for col in range(cols)] for row in range(rows)])


def matrix_make_empty(cols, rows):
    return matrix_make(cols, rows, lambda col, row: EL_EMPTY)


def matrix_make_incremental(cols, rows):
    return matrix_make(cols, rows, lambda col, row: cols * col + row % cols)


def pick_dimension():
    while True:
        answer = ask.open_question('', str).split()
        try:
            if len(answer) == 2:
                return [int(el) for el in answer]
        except ValueError:
            continue


def main():
    def game_over():
        print()
        print(MSG_GAME_OVER)
        menu.go_out()

    def is_game_over():
        return len([el for el in board[0] if el == EL_OCCUPIED]) > 0

    def matrix_show(matrix):
        print()
        print(matrix_to_string(matrix))
        print()

    def board_show():
        matrix_show(board)

    vector_zero = np.array([0, 0, 0, 0])

    # init values
    cols, rows = pick_dimension()
    board = matrix_make_empty(cols, rows)
    board_show()

    # shape init values
    position = 0
    shape_letter = None
    shape_positions = []
    shape = np.array([])
    shape_positions_length = 0
    vector_sum = vector_zero

    def matrix_draw_shape(shape_arg, store=False):
        matrix_indices = matrix_make_incremental(cols, rows)
        matrix = board if store else deepcopy(board)
        for ind in shape_arg:
            x = np.where(matrix_indices == ind)[0][0]
            y = np.where(matrix_indices == ind)[1][0]
            matrix[x][y] = EL_OCCUPIED
        return matrix

    def shape_choose():
        nonlocal shape_letter, shape_positions, shape, shape_positions_length, position, vector_sum
        position = 0
        shape_letter = ask.closed_str('', SHAPE_POSITIONS.keys())
        shape = np.array(SHAPE_POSITIONS[shape_letter][position])
        shape_positions = SHAPE_POSITIONS[shape_letter]
        shape_positions_length = len(shape_positions)
        vector_sum = vector_zero

        hits_bottom = hit_bottom(shape + vector_sum)

        matrix_show(matrix_draw_shape(shape, hits_bottom))

    def matrix_store_shape(shape_arg):
        matrix_draw_shape(shape_arg, True)

    def is_outside_left(vector):
        vector_rests = [val % cols for val in vector]
        return min(vector_rests) <= 0

    def is_outside_right(vector):
        vector_rests = [val % cols for val in vector]
        return max(vector_rests) >= cols - 1

    def hit_bottom(vector):
        if max([int((el / cols)) for el in vector]) >= rows - 1:
            return True
        return len([el for el in vector if board[int(((el - (el % rows)) / cols)) + 1][el % cols] == EL_OCCUPIED])

    def board_print():
        print(matrix_to_string(board))

    def shape_move(vector):
        nonlocal shape, vector_sum, vector_zero

        if hit_bottom(shape + vector_sum):
            matrix_store_shape(shape + vector_sum)
            board_print()
            if is_game_over():
                game_over()
            return

        vector_sum = vector_sum \
                     + vector \
                     + (np.array([0, 0, 0, 0]) if hit_bottom(shape + vector_sum) else vector_down(cols))

        if hit_bottom(shape + vector_sum):
            matrix_store_shape(shape + vector_sum)
            if is_game_over():
                board_print()
                game_over()

        print(matrix_to_string(matrix_draw_shape(shape + vector_sum)))
        if is_game_over():
            game_over()

    def down():
        shape_move(np.array([0, 0, 0, 0]))

    def left():
        shape_move(vector_zero if is_outside_left(shape + vector_sum) else VECTOR_LEFT)

    def right():
        shape_move(vector_zero if is_outside_right(shape + vector_sum) else VECTOR_RIGHT)

    def is_row_filled():
        return ''.join(board[rows - 1]) == ''.join([EL_OCCUPIED for _ in range(cols)])

    def erase():
        nonlocal board, cols
        if not is_row_filled():
            return
        dboard = deque(board)
        dboard.pop()
        dboard.appendleft(np.array(['- ' for _ in range(cols)]))
        board = np.array(list(dboard))
        erase()

    def board_erase():
        erase()
        board_print()

    def rotate():
        nonlocal position, vector_sum, shape
        if hit_bottom(shape + vector_sum):
            shape_move(vector_zero)
            return

        position_next = (position + 1) % shape_positions_length
        shape_next = np.array(SHAPE_POSITIONS[shape_letter][position_next])

        if hit_bottom(shape_next + vector_sum):
            shape_move(vector_zero)
            return

        position = position_next
        shape = shape_next
        shape_move(vector_zero)

    menu.init({
        COMMAND_ROTATE: rotate,
        COMMAND_LEFT: left,
        COMMAND_RIGHT: right,
        COMMAND_DOWN: down,
        COMMAND_EXIT: lambda: menu.go_out(),
        'r': rotate,
        '<': left,
        '>': right,
        'd': down,
        'q': lambda: menu.go_out(),
        'b': lambda: menu.go_out(),
        'n': shape_choose,
        'piece': shape_choose,
        'c': board_erase,
        'break': board_erase,
    }, '')


if __name__ == '__main__':
    main()

from typing import List
from game.slot_states import SlotState
import copy


def to_str(board: List[List[SlotState]]) -> str:
    num_rows = len(board)
    num_cols = len(board[0])

    drawing = ""
    drawing += "===== START BOARD IMAGE =====\n"
    for row in range(num_rows):
        current_row_str = ""
        for col in range(num_cols):
            current_row_str += board[row][col].to_char()
            if col != num_cols - 1:
                current_row_str += " "
        drawing += current_row_str + "\n"
    drawing += "====== END BOARD IMAGE ======"
    return drawing


def from_char_matrix(image: List[List[str]]) -> List[List[SlotState]]:
    num_rows = len(image)
    num_cols = len(image[0])

    board = [[None]*num_cols for row in range(num_rows)]
    for row in range(num_rows):
        for col in range(num_cols):
            board[row][col] = SlotState.from_char(image[row][col])
    return board

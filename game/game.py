from game.slot_states import SlotState
from game.outcome import Outcome
import game.board_utils as board_utils
from typing import List, Set, Tuple
import copy


class Game:
    def __init__(self, num_rows=8, num_cols=9, line_length_to_win=4):
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._line_length_to_win = line_length_to_win
        self.start_new()

    def start_new(self):
        self._board: List[SlotState] = [
            [SlotState.EMPTY] * self._num_cols for row in range(self._num_rows)
        ]
        self._p1_to_move = True
        self._outcome = Outcome.ONGOING

    def get_board(self) -> List[List[SlotState]]:
        return copy.deepcopy(self._board)

    def at_pos(self, pos: Tuple[int, int]) -> SlotState:
        row, col = pos
        return self._board[row][col]

    def is_p1_to_move(self) -> bool:
        return self._p1_to_move

    def get_outcome(self) -> Outcome:
        return self._outcome

    def get_legal_moves(self) -> Set[int]:
        legal_moves = set()
        top_row = self._board[0]
        for i, slot in enumerate(top_row):
            if slot == SlotState.EMPTY:
                legal_moves.add(i)
        return legal_moves

    def get_col(self, col) -> List[SlotState]:
        return [row[col] for row in self._board]

    def col_exists(self, col: int) -> bool:
        return col >= 0 and col < self._num_cols

    def row_exists(self, row: int) -> bool:
        return row >= 0 and row < self._num_rows

    def pos_exists(self, pos: Tuple[int, int]) -> bool:
        return self.row_exists(pos[0]) and self.col_exists(pos[1])

    ###
    ### Check if the given player has a line which includes the given position
    ###
    def player_has_line(self, check_for_p1: bool, with_pos: Tuple[int, int]):
        slot_type = SlotState.PLAYER_1 if check_for_p1 else SlotState.PLAYER_2
        pos_row, pos_col = with_pos

        if self._board[pos_row][pos_col] != slot_type:
            return False

        steps_to_try = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for step in steps_to_try:
            line_length = 1

            step_row = step[0]
            step_col = step[1]
            cur_row = pos_row + step_row
            cur_col = pos_col + step_col
            while (
                self.pos_exists((cur_row, cur_col))
                and self._board[cur_row][cur_col] == slot_type
            ):
                line_length += 1
                cur_row += step_row
                cur_col += step_col

            reverse_step_row = -1 * step_row
            reverse_step_col = -1 * step_col
            cur_row = pos_row + reverse_step_row
            cur_col = pos_col + reverse_step_col
            while (
                self.pos_exists((cur_row, cur_col))
                and self._board[cur_row][cur_col] == slot_type
            ):
                line_length += 1
                cur_row += reverse_step_row
                cur_col += reverse_step_col

            if line_length >= self._line_length_to_win:
                return True

        return False

    def play_move(self, move: int):
        if self.get_outcome() != Outcome.ONGOING:
            raise Exception(
                "Tried to play move {} in finished game".format(move)
            )
        if move < 0:
            raise Exception("Tried to play negative move {}".format(move))
        if move >= self._num_cols:
            raise Exception(
                "Tried to play move {} but board only has {} columns".format(
                    move, self._num_cols
                )
            )
        if self._board[0][move] != SlotState.EMPTY:
            err_msg = "Tried to illegally play move {} in the following position: \n{}".format(
                move, board_utils.to_str(self._board)
            )
            raise Exception(err_msg)
        row = 0
        while (
            row != self._num_rows - 1
            and self._board[row + 1][move] == SlotState.EMPTY
        ):
            row += 1
        self._board[row][move] = (
            SlotState.PLAYER_1 if self._p1_to_move else SlotState.PLAYER_2
        )
        self._p1_to_move = not self._p1_to_move

        pos_just_played = (row, move)
        p1_just_played = not self._p1_to_move
        if self.player_has_line(p1_just_played, pos_just_played):
            self._outcome = (
                Outcome.PLAYER_1_WIN
                if p1_just_played
                else Outcome.PLAYER_2_WIN
            )
        elif not self.get_legal_moves():
            self._outcome = Outcome.DRAW

import unittest
from game.game import Game
from game.slot_states import SlotState
from game.outcome import Outcome
import game.board_utils as board_utils


class TestGame(unittest.TestCase):
    def setUp(self):
        pass

    def test_fresh_game(self):
        game = Game(num_rows=8, num_cols=9, line_length_to_win=4)
        self.assertListEqual(
            game.get_board(),
            board_utils.from_char_matrix(
                [
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                ]
            ),
        )
        self.assertTrue(game.is_p1_to_move())
        self.assertEqual(game.get_outcome(), Outcome.ONGOING)
        self.assertListEqual(game.get_move_history(), [])

    def test_play_moves(self):
        game = Game(num_rows=8, num_cols=9, line_length_to_win=4)
        game.play_move(0)
        game.play_move(0)
        game.play_move(4)
        game.play_move(2)
        game.play_move(4)
        game.play_move(8)
        game.play_move(8)
        game.play_move(8)
        for i in range(8):
            game.play_move(7)
        self.assertListEqual(
            game.get_board(),
            board_utils.from_char_matrix(
                [
                    ["-", "-", "-", "-", "-", "-", "-", "O", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "X", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "O", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "X", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "O", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "X", "O"],
                    ["O", "-", "-", "-", "X", "-", "-", "O", "X"],
                    ["X", "-", "O", "-", "X", "-", "-", "X", "O"],
                ]
            ),
        )
        self.assertTrue(game.is_p1_to_move())
        self.assertEqual(game.get_outcome(), Outcome.ONGOING)

    def test_start_new(self):
        game = Game(num_rows=8, num_cols=9, line_length_to_win=4)
        game.play_move(0)
        game.play_move(0)
        game.play_move(4)
        game.play_move(2)
        game.start_new()
        self.assertListEqual(
            game.get_board(),
            board_utils.from_char_matrix(
                [
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                ]
            ),
        )
        self.assertTrue(game.is_p1_to_move())
        self.assertEqual(game.get_outcome(), Outcome.ONGOING)
        self.assertListEqual(game.get_move_history(), [])

    def test_player_1_to_move(self):
        game = Game(num_rows=8, num_cols=9, line_length_to_win=4)
        game.play_move(1)
        game.play_move(7)
        game.play_move(4)
        game.play_move(7)
        self.assertTrue(game.is_p1_to_move())

    def test_player_2_to_move(self):
        game = Game(num_rows=8, num_cols=9, line_length_to_win=4)
        game.play_move(1)
        game.play_move(7)
        game.play_move(4)
        game.play_move(7)
        game.play_move(7)
        self.assertFalse(game.is_p1_to_move())

    def test_exceed_max_height(self):
        game = Game(num_rows=8, num_cols=9, line_length_to_win=4)
        for i in range(8):
            game.play_move(7)
        with self.assertRaisesRegex(
            Exception, r"Tried to illegally play move 7"
        ):
            game.play_move(7)

    def test_negative_move(self):
        game = Game(num_rows=8, num_cols=9, line_length_to_win=4)
        with self.assertRaisesRegex(
            Exception, r"Tried to play move 9 but board only has 9 columns"
        ):
            game.play_move(9)

    def test_move_too_large(self):
        game = Game(num_rows=8, num_cols=9, line_length_to_win=4)
        with self.assertRaisesRegex(
            Exception, r"Tried to play move 9 but board only has 9 columns"
        ):
            game.play_move(9)

    def test_get_legal_moves(self):
        game = Game(num_rows=8, num_cols=9, line_length_to_win=4)
        game.play_move(2)
        for i in range(7):
            game.play_move(1)
        for i in range(8):
            game.play_move(7)
            game.play_move(0)
            game.play_move(5)
        self.assertSetEqual(game.get_legal_moves(), {1, 2, 3, 4, 6, 8})

    def test_p1_win_vertical(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [0, 1, 1, 2, 1, 2, 1]
        for move in moves:
            game.play_move(move)
        self.assertEqual(game.get_outcome(), Outcome.PLAYER_1_WIN)

    def test_p1_win_horizontal(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [0, 1, 2, 3, 0, 3, 1, 0, 2]
        for move in moves:
            game.play_move(move)
        self.assertEqual(game.get_outcome(), Outcome.PLAYER_1_WIN)

    def test_p1_win_diagonal_up(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [1, 2, 2, 3, 3, 0, 3]
        for move in moves:
            game.play_move(move)
        self.assertEqual(game.get_outcome(), Outcome.PLAYER_1_WIN)

    def test_p1_win_diagonal_down(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [3, 2, 2, 1, 1, 3, 1]
        for move in moves:
            game.play_move(move)
        self.assertEqual(game.get_outcome(), Outcome.PLAYER_1_WIN)

    def test_p2_win_vertical(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [0, 2, 1, 2, 0, 2]
        for move in moves:
            game.play_move(move)
        self.assertEqual(game.get_outcome(), Outcome.PLAYER_2_WIN)

    def test_p2_win_horizontal(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [0, 1, 2, 3, 3, 2, 2, 1, 3, 0]
        for move in moves:
            game.play_move(move)
        self.assertEqual(game.get_outcome(), Outcome.PLAYER_2_WIN)

    def test_p2_win_diagonal_up(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [0, 1, 2, 3, 3, 2, 2, 1, 3, 0]
        for move in moves:
            game.play_move(move)
        self.assertEqual(game.get_outcome(), Outcome.PLAYER_2_WIN)

    def test_draw(self):
        game = Game(num_rows=8, num_cols=9, line_length_to_win=4)
        moves = [0, 1, 0, 1, 0, 1, 2, 3, 2, 3, 2, 3, 4, 5, 4, 5, 4, 5, 6]
        moves += [7, 6, 7, 6, 7, 8, 0, 8, 0, 8, 0, 1, 2, 1, 2, 1, 2, 3, 4]
        moves += [3, 4, 3, 4, 5, 6, 5, 6, 5, 6, 7, 8, 7, 8, 7, 8, 0, 1, 0]
        moves += [1, 2, 3, 2, 3, 4, 5, 4, 5, 6, 7, 6, 7, 8, 8]
        for move in moves:
            game.play_move(move)
        self.assertEqual(game.get_outcome(), Outcome.DRAW)

    def test_p1_win_on_last_move(self):
        game = Game(num_rows=3, num_cols=3, line_length_to_win=3)
        moves = [0, 1, 2, 1, 1, 0, 2, 0, 2]
        for move in moves:
            game.play_move(move)
        self.assertEqual(game.get_outcome(), Outcome.PLAYER_1_WIN)

    def test_p2_win_on_last_move(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [0, 0, 0, 0, 2, 1, 2, 1, 1, 2, 1, 3, 2, 3, 3, 3]
        for move in moves:
            game.play_move(move)
        self.assertEqual(game.get_outcome(), Outcome.PLAYER_2_WIN)

    def test_start_new_after_p1_win(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [0, 1, 1, 2, 1, 2, 1]
        for move in moves:
            game.play_move(move)
        game.start_new()
        self.assertListEqual(
            game.get_board(),
            board_utils.from_char_matrix(
                [
                    ["-", "-", "-", "-"],
                    ["-", "-", "-", "-"],
                    ["-", "-", "-", "-"],
                    ["-", "-", "-", "-"],
                ]
            ),
        )
        self.assertTrue(game.is_p1_to_move())
        self.assertEqual(game.get_outcome(), Outcome.ONGOING)
        self.assertListEqual(game.get_move_history(), [])

    def test_start_new_after_p2_win(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [0, 2, 1, 2, 0, 2]
        for move in moves:
            game.play_move(move)
        game.start_new()
        self.assertListEqual(
            game.get_board(),
            board_utils.from_char_matrix(
                [
                    ["-", "-", "-", "-"],
                    ["-", "-", "-", "-"],
                    ["-", "-", "-", "-"],
                    ["-", "-", "-", "-"],
                ]
            ),
        )
        self.assertTrue(game.is_p1_to_move())
        self.assertEqual(game.get_outcome(), Outcome.ONGOING)
        self.assertListEqual(game.get_move_history(), [])

    def test_start_new_after_draw(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [0, 0, 0, 0, 2, 1, 2, 1, 1, 2, 1, 3, 3, 3, 3, 2]
        for move in moves:
            game.play_move(move)
        game.start_new()
        self.assertListEqual(
            game.get_board(),
            board_utils.from_char_matrix(
                [
                    ["-", "-", "-", "-"],
                    ["-", "-", "-", "-"],
                    ["-", "-", "-", "-"],
                    ["-", "-", "-", "-"],
                ]
            ),
        )
        self.assertTrue(game.is_p1_to_move())
        self.assertEqual(game.get_outcome(), Outcome.ONGOING)
        self.assertListEqual(game.get_move_history(), [])

    def test_play_move_after_p1_win(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [0, 1, 1, 2, 1, 2, 1]
        for move in moves:
            game.play_move(move)
        with self.assertRaisesRegex(
            Exception, r"Tried to play move 0 in finished game"
        ):
            game.play_move(0)

    def test_play_move_after_p2_win(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [0, 2, 1, 2, 0, 2]
        for move in moves:
            game.play_move(move)
        with self.assertRaisesRegex(
            Exception, r"Tried to play move 1 in finished game"
        ):
            game.play_move(1)

    def test_play_move_after_draw(self):
        game = Game(num_rows=4, num_cols=4, line_length_to_win=3)
        moves = [0, 0, 0, 0, 2, 1, 2, 1, 1, 2, 1, 3, 3, 3, 3, 2]
        for move in moves:
            game.play_move(move)
        with self.assertRaisesRegex(
            Exception, r"Tried to play move 2 in finished game"
        ):
            game.play_move(2)

    def test_move_history_partial_game(self):
        game = Game(num_rows=8, num_cols=9, line_length_to_win=4)
        moves = [1, 7, 7, 2, 1, 0, 2, 2, 2, 2, 3, 2]
        for move in moves:
            game.play_move(move)
        self.assertListEqual(game.get_move_history(), moves)

    def test_move_history_full_game(self):
        game = Game(num_rows=8, num_cols=9, line_length_to_win=4)
        moves = [0, 1, 0, 1, 0, 1, 2, 3, 2, 3, 2, 3, 4, 5, 4, 5, 4, 5, 6]
        moves += [7, 6, 7, 6, 7, 8, 0, 8, 0, 8, 0, 1, 2, 1, 2, 1, 2, 3, 4]
        moves += [3, 4, 3, 4, 5, 6, 5, 6, 5, 6, 7, 8, 7, 8, 7, 8, 0, 1, 0]
        moves += [1, 2, 3, 2, 3, 4, 5, 4, 5, 6, 7, 6, 7, 8, 8]
        for move in moves:
            game.play_move(move)
        self.assertListEqual(game.get_move_history(), moves)

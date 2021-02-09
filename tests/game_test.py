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

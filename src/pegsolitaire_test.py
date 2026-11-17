import unittest
import tkinter as tk
from unittest.mock import patch
from pegsolitaire import Game, BoardUI

class TestChooseBoardSize(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = BoardUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_select_9(self):
        self.app.size_dropdown.set("9")

        self.assertEqual(self.app.size_dropdown.get(), "9")

    def test_select_7(self):
        self.app.size_dropdown.set("7")

        self.assertEqual(self.app.size_dropdown.get(),"7")

class TestChooseBoardType(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = BoardUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_select_hexagon(self):
        self.app.type_var.set("Hexagon")

        self.assertEqual(self.app.type_var.get(),"Hexagon")

    def test_select_english(self):
        self.app.type_var.set("English")

        self.assertEqual(self.app.type_var.get(),"English")

class TestChooseGameMode(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = BoardUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_manual_default(self):
        self.assertFalse(self.app.auto_playing)

    def test_choose_automated(self):
        self.app.start_auto_play()

        self.assertTrue(self.app.auto_playing)

class TestStartGame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = BoardUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_valid_board_manual(self):
        self.app.size_dropdown.set("9")
        self.app.type_var.set("Hexagon")

        self.app.new_game()

        self.assertEqual(self.app.game.board_size, 9)
        self.assertEqual(len(self.app.game.board), 9)
        self.assertEqual(len(self.app.game.board[0]), 9)
        self.assertEqual(self.app.type_var.get(), "Hexagon")
        self.assertFalse(self.app.auto_playing)

    def test_no_size_selected(self):
        self.app.type_var.set("Hexagon")

        self.app.new_game()

        self.assertEqual(self.app.game.board_size, 7)
        self.assertEqual(len(self.app.game.board), 7)
        self.assertEqual(len(self.app.game.board[0]), 7)
        self.assertEqual(self.app.type_var.get(), "Hexagon")
        self.assertFalse(self.app.auto_playing)

    def test_no_type_selected(self):
        self.app.size_dropdown.set("9")

        self.app.new_game()

        self.assertEqual(self.app.game.board_size, 9)
        self.assertEqual(len(self.app.game.board), 9)
        self.assertEqual(len(self.app.game.board[0]), 9)
        self.assertEqual(self.app.type_var.get(), "English")
        self.assertFalse(self.app.auto_playing)

    def test_default_start(self):
        self.app.new_game()

        self.assertEqual(self.app.game.board_size, 7)
        self.assertEqual(len(self.app.game.board), 7)
        self.assertEqual(len(self.app.game.board[0]), 7)
        self.assertEqual(self.app.type_var.get(), "English")
        self.assertFalse(self.app.auto_playing)

    def test_valid_board_automated(self):
        self.app.size_dropdown.set("9")
        self.app.type_var.set("Hexagon")

        self.app.start_auto_play()

        self.assertEqual(self.app.game.board_size, 7)
        self.assertEqual(len(self.app.game.board), 7)
        self.assertEqual(len(self.app.game.board[0]), 7)
        self.assertEqual(self.app.type_var.get(), "Hexagon")
        self.assertTrue(self.app.auto_playing)

class TestMakeMove(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = BoardUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_valid_move(self):
        self.app.new_game()
        start = (3, 1)
        destination = (3, 3)

        valid_moves = self.app.game.get_valid_moves(*start)

        self.assertIn(destination, valid_moves)

        self.app.game.make_move(start, destination)

        self.assertEqual(self.app.game.board[3][1], "empty")
        self.assertEqual(self.app.game.board[3][2], "empty")
        self.assertEqual(self.app.game.board[3][3], "peg")

    def test_invalid_move(self):
        self.app.new_game()
        start = (3, 2)
        destination = (3, 4)

        original_board = [row.copy() for row in self.app.game.board]

        self.app.game.make_move(start, destination)

        self.assertEqual(original_board, self.app.game.board)

class TestGameOver(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = BoardUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_no_valid_moves(self):
        self.app.game.board = [
            ["empty" for _ in range(self.app.game.board_size)]
            for _ in range(self.app.game.board_size)
        ]
        self.app.game.board[3][0] = "peg"
        self.app.game.board[0][3] = "peg"

        self.assertTrue(self.app.game.is_game_over())

        self.app.show_game_over()

        messages = self.app.canvas.find_all()

        displayed_text = [
            self.app.canvas.itemcget(item, "text")
            for item in messages
            if self.app.canvas.type(item) == "text"
        ]

        self.assertIn("GAME OVER", displayed_text)

    def test_player_wins(self):
        self.app.game.board = [
            ["empty" for _ in range(self.app.game.board_size)]
            for _ in range(self.app.game.board_size)
        ]
        self.app.game.board[3][1] = "peg"
        self.app.game.board[3][2] = "peg"

        self.app.game.make_move((3, 1), (3, 3))

        self.assertTrue(self.app.game.player_wins())

        self.app.show_game_over()

        messages = self.app.canvas.find_all()

        displayed_text = [
            self.app.canvas.itemcget(item, "text")
            for item in messages
            if self.app.canvas.type(item) == "text"
        ]

        self.assertIn("YOU WIN!", displayed_text)

class TestAutoPlayMove(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = BoardUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_random_move_is_valid(self):
        move = self.app.game.get_random_move()

        self.assertIsNotNone(move)

        start, destination = move
        valid_moves = self.app.game.get_valid_moves(*start)

        self.assertIn(destination, valid_moves)

class TestAutoPlayGameOver(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = BoardUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_no_random_move_available(self):
        for r in range(self.app.game.board_size):
            for c in range(self.app.game.board_size):
                if self.app.game.is_playable(r, c):
                    self.app.game.board[r][c] = "empty"

        self.app.game.board[3][3] = "peg"
        self.app.game.board[4][2] = "peg"

        move = self.app.game.get_random_move()

        self.assertIsNone(move)

        self.app.show_game_over()

        messages = self.app.canvas.find_all()

        displayed_text = [
            self.app.canvas.itemcget(item, "text")
            for item in messages
            if self.app.canvas.type(item) == "text"
        ]

        self.assertIn("GAME OVER", displayed_text)

    def test_autoplay_win(self):
        self.app.game.board[2][2] = "peg"
        self.app.game.board[2][3] = "peg"

        for r in range(7):
            for c in range(7):
                if (r, c) not in [(2, 2), (2, 3)]:
                    if self.app.game.is_playable(r, c):
                        self.app.game.board[r][c] = "empty"

        self.app.auto_playing = True

        with patch.object(
                self.app.game,
                "get_random_move",
                return_value=((2, 2), (2, 4))
        ):
            with patch.object(
                    self.app,
                    "show_game_over"
            ) as mock_game_over:
                self.app.play_random_move()

                self.assertTrue(self.app.game.player_wins())

                self.assertFalse(self.app.auto_playing)

                mock_game_over.assert_called_once()

        self.app.show_game_over()

        messages = self.app.canvas.find_all()

        displayed_text = [
            self.app.canvas.itemcget(item, "text")
            for item in messages
            if self.app.canvas.type(item) == "text"
        ]

        self.assertIn("YOU WIN!", displayed_text)

class TestRandomizeBoard(unittest.TestCase):
    def setUp(self):
        self.game = Game(7, "English")

        self.root = tk.Tk()
        self.root.withdraw()
        self.app = BoardUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_randomize_board(self):
        original_board = [row.copy() for row in self.game.board]

        self.game.randomize_board()

        self.assertNotEqual(self.game.board, original_board)

if __name__ == '__main__':
    unittest.main()
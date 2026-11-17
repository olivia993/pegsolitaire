import tkinter as tk
from tkinter import ttk
import random

class Game:
    def __init__(self, board_size=7, board_type="English"):
        self.board_size = board_size
        self.board_type = board_type

        self.board = []
        self.initialize_board()

    def initialize_board(self):
        self.board = [
            [None for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]

        for r in range(self.board_size):
            for c in range(self.board_size):

                if self.is_playable(r, c):
                    if (r == self.board_size // 2 and
                            c == self.board_size // 2):
                        self.board[r][c] = "empty"
                    else:
                        self.board[r][c] = "peg"

    def randomize_board(self):
        playable_cells = []

        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.is_playable(r, c):
                    playable_cells.append((r, c))

        states = [
            self.board[r][c]
            for r, c in playable_cells
        ]

        random.shuffle(states)

        for (r, c), state in zip(playable_cells, states):
            self.board[r][c] = state

    def is_playable(self, r, c):
        center = self.board_size // 2

        if self.board_type == "English":
            return (
                    abs(r - center) <= 1 or
                    abs(c - center) <= 1
            )

        elif self.board_type == "Hexagon":
            return (
                    abs(r - center) <= center
                    and abs(c - center) <= center
                    and abs(r - center) + abs(c - center) <= center + 1
            )

        return False

    def get_valid_moves(self, r, c):
        moves = {}

        if self.board[r][c] != "peg":
            return moves

        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            jr, jc = nr + dr, nc + dc

            if ((0 <= nr < self.board_size and 0 <= nc < self.board_size and
                    (0 <= jr < self.board_size and 0 <= jc < self.board_size)) and
                    self.is_playable(nr, nc) and
                    self.is_playable(jr, jc)):

                if (self.board[nr][nc] == "peg" and
                        self.board[jr][jc] == "empty"):

                    moves[(jr, jc)] = (nr, nc)

        return moves

    def make_move(self, start, destination):
        start_r, start_c = start
        r, c = destination

        valid_moves = self.get_valid_moves(start_r, start_c)

        if destination not in valid_moves:
            return False

        cap_r, cap_c = valid_moves[destination]

        self.board[r][c] = "peg"
        self.board[start_r][start_c] = "empty"
        self.board[cap_r][cap_c] = "empty"

        return True

    def is_game_over(self):
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == "peg":
                    if self.get_valid_moves(r, c):
                        return False

        return True

    def player_wins(self):
        peg_count = sum(
            1
            for row in self.board
            for cell in row
            if cell == "peg"
        )

        return self.is_game_over() and peg_count == 1

    def get_random_move(self):
        all_moves = []

        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == "peg":
                    valid_moves = self.get_valid_moves(r, c)

                    for destination in valid_moves:
                        all_moves.append(((r, c), destination))

        if not all_moves:
            return None

        return random.choice(all_moves)

class BoardUI:
    def __init__(self, root):
        self.root = root
        self.cell_size = 50
        self.board_size = 7

        self.selected_piece = None
        self.valid_moves = {}

        self.auto_playing = False
        self.after_id = None

        self.game = Game()

        self.title_label = tk.Label(
            root,
            text="Peg Solitaire",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=5)

        controls = tk.Frame(root)
        controls.pack(pady=5)

        radiobuttons = tk.Frame(controls, width=10, height=15)
        radiobuttons.pack(side=tk.LEFT)

        tk.Label(radiobuttons, text="Board Type:").pack(anchor="w")
        self.type_var = tk.StringVar(value="English")

        english = ttk.Radiobutton(
            radiobuttons,
            text="English",
            variable=self.type_var,
            value="English"
        )
        english.pack(anchor="w", padx=5)

        hexagon = ttk.Radiobutton(
            radiobuttons,
            text="Hexagon",
            variable=self.type_var,
            value="Hexagon"
        )
        hexagon.pack(anchor="w", padx=5)

        self.board_types = [english, hexagon]

        tk.Label(controls, text="Board Size:").pack(side=tk.LEFT, padx=5)
        self.size_var = tk.StringVar(value="7")
        self.size_dropdown = ttk.Combobox(
            controls,
            textvariable=self.size_var,
            values=["7", "9"],
            state="readonly",
            width=5
        )
        self.size_dropdown.pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls,
            text="New Game",
            command=self.new_game
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls,
            text="Autoplay",
            command=self.start_auto_play
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls,
            text="Randomize Board",
            command=self.randomize_game
        ).pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(
            root,
            width=self.board_size * self.cell_size,
            height=self.board_size * self.cell_size,
            borderwidth=0,
            highlightthickness=0
        )

        self.canvas.pack(padx=40, pady=10)
        self.canvas.bind("<Button-1>", self.handle_click)

        self.draw_board()

    def new_game(self):
        board_size = int(self.size_var.get())
        board_type = self.type_var.get()

        self.game = Game(board_size, board_type)

        self.selected_piece = None
        self.valid_moves = {}

        self.canvas.config(
            width=board_size * self.cell_size,
            height=board_size * self.cell_size
        )

        self.title_label.config(
            text=f"Peg Solitaire - {board_type} ({board_size}x{board_size})"
        )

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")

        for r in range(self.game.board_size):
            for c in range(self.game.board_size):

                if not self.game.is_playable(r, c):
                    continue

                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="white",
                    outline="black",
                    width=2
                )

                piece = self.game.board[r][c]

                if piece == "peg":
                    self.canvas.create_oval(
                        x1 + 13, y1 + 13,
                        x2 - 13, y2 - 13,
                        fill="black",
                        outline="gold" if self.selected_piece == (r, c)
                        else "black",
                        width=2 if self.selected_piece == (r, c) else 1
                    )

                if (r, c) in self.valid_moves:
                    self.canvas.create_oval(
                        x1 + 16, y1 + 16,
                        x2 - 16, y2 - 16,
                        fill="green",
                        outline=""
                    )

    def handle_click(self, event):
        if self.auto_playing:
            return

        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if not (0 <= row < self.game.board_size and
                0 <= col < self.game.board_size):
            return

        if self.selected_piece is not None and (row, col) in self.valid_moves:

            self.game.make_move(
                self.selected_piece,
                (row, col)
            )

            self.selected_piece = None
            self.valid_moves = {}

        elif self.game.board[row][col] == "peg":

            self.selected_piece = (row, col)

            self.valid_moves = self.game.get_valid_moves(row, col)

        else:
            self.selected_piece = None
            self.valid_moves = {}

        self.draw_board()

        if self.game.is_game_over():
            self.show_game_over()

    def show_game_over(self):
        if self.game.player_wins():
            message = "YOU WIN!"
            color = "green"
        else:
            message = "GAME OVER"
            color = "red"

        center = self.game.board_size * self.cell_size // 2

        self.canvas.create_rectangle(
            center - 120, center - 35,
            center + 120, center + 35,
            fill="white",
            outline="black",
            width=2
        )

        self.canvas.create_text(
            center, center,
            text=message,
            font=("Arial", 24, "bold"),
            fill=color
        )

    def start_auto_play(self):
        if self.auto_playing:
            return

        self.auto_playing = True
        self.play_random_move()

    def play_random_move(self):
        if not self.auto_playing:
            return

        move = self.game.get_random_move()

        if move is None:
            self.auto_playing = False
            self.show_game_over()
            return

        start, destination = move

        self.game.make_move(start, destination)

        self.draw_board()

        if self.game.player_wins():
            self.auto_playing = False
            self.show_game_over()
            return

        self.after_id = self.root.after(
            500,
            self.play_random_move
        )

    def randomize_game(self):
        if self.auto_playing:
            return

        self.game.randomize_board()

        self.selected_piece = None
        self.valid_moves = {}

        self.draw_board()

        if self.game.is_game_over():
            self.show_game_over()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Peg Solitaire")

    app = BoardUI(root)

    root.mainloop()
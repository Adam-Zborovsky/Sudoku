import tkinter as tk
from tkinter import ttk
from constants.settings import WINDOW_SIZE, WINDOW_BG, DIFFICULTY_LEVELS
from .grid import SudokuGrid
from .controls import ControlPanel


class SudokuWindow:
    def __init__(self, game_logic):
        self.root = tk.Tk()
        # Attach the SudokuWindow instance to the root.
        # This allows other parts of the code to access the window's methods.
        self.root.window = self

        self.game_logic = game_logic
        self.setup_window()
        self.setup_styles()

        # Create main container
        self.main_frame = tk.Frame(self.root, bg=WINDOW_BG)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Start with difficulty selection
        self.show_difficulty_selection()

    def setup_window(self):
        self.root.title("Sudoku")
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=WINDOW_BG)

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Rounded.TButton',
                             padding=6,
                             relief="flat",
                             background="#4a90e2",
                             foreground="white",
                             font=('Helvetica', 10))

    def show_difficulty_selection(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create difficulty buttons
        difficulty_frame = tk.Frame(self.main_frame, bg=WINDOW_BG)
        difficulty_frame.pack(expand=True)

        tk.Label(
            difficulty_frame,
            text="Select Difficulty",
            font=('Helvetica', 16, 'bold'),
            bg=WINDOW_BG
        ).pack(pady=(0, 20))

        for difficulty in DIFFICULTY_LEVELS:
            ttk.Button(
                difficulty_frame,
                text=difficulty,
                style='Rounded.TButton',
                command=lambda d=difficulty: self.start_game(d)
            ).pack(pady=5)

    def start_game(self, difficulty):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Start new game and generate puzzle
        puzzle = self.game_logic.start_new_game(difficulty)

        # Create the Sudoku grid with a fixed height to leave room for additional controls
        self.grid = SudokuGrid(self.main_frame, self.game_logic)
        self.grid.frame.config(height=600)  # Set fixed height for the board
        # Prevent frame auto-resizing to its content
        self.grid.frame.pack_propagate(False)
        self.grid.frame.pack(fill='x', padx=10, pady=(10, 0))
        self.grid.fill_grid(puzzle)

        # Create control panel (which now includes the highlight toggle)
        self.controls = ControlPanel(self.main_frame, self.game_logic)
        self.controls.frame.pack(fill='x', pady=(20, 0))

    def run(self):
        self.root.mainloop()

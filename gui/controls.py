import tkinter as tk
from tkinter import ttk
from constants.settings import COLORS
from gui.widgets.toggle_button import RoundToggleButton


class ControlPanel:
    def __init__(self, parent, game_logic):
        self.frame = tk.Frame(parent)
        self.game_logic = game_logic
        self.parent = parent
        self.create_controls()
        self.frame.pack(pady=10)

    def create_controls(self):
        # --- Add a row for the individual highlight toggles ---
        highlight_toggles_frame = tk.Frame(self.frame)
        highlight_toggles_frame.pack(fill='x', padx=5, pady=(0, 10))

        # Row Highlight Toggle
        row_toggle_frame = tk.Frame(highlight_toggles_frame)
        row_toggle_frame.pack(side=tk.LEFT, expand=True)
        tk.Label(row_toggle_frame, text="Row",
                 font=('Arial', 10)).pack(side=tk.TOP)
        self.row_toggle = RoundToggleButton(
            row_toggle_frame, command=self.toggle_row_highlight)
        self.row_toggle.pack(side=tk.TOP, pady=2)
        # (Default will be synced below)

        # Column Highlight Toggle
        column_toggle_frame = tk.Frame(highlight_toggles_frame)
        column_toggle_frame.pack(side=tk.LEFT, expand=True)
        tk.Label(column_toggle_frame, text="Column",
                 font=('Arial', 10)).pack(side=tk.TOP)
        self.column_toggle = RoundToggleButton(
            column_toggle_frame, command=self.toggle_column_highlight)
        self.column_toggle.pack(side=tk.TOP, pady=2)

        # Box Highlight Toggle (box highlighting off by default)
        box_toggle_frame = tk.Frame(highlight_toggles_frame)
        box_toggle_frame.pack(side=tk.LEFT, expand=True)
        tk.Label(box_toggle_frame, text="Box",
                 font=('Arial', 10)).pack(side=tk.TOP)
        self.box_toggle = RoundToggleButton(
            box_toggle_frame, command=self.toggle_box_highlight)
        self.box_toggle.pack(side=tk.TOP, pady=2)

        # Match Highlight Toggle (for same-number matching outline)
        match_toggle_frame = tk.Frame(highlight_toggles_frame)
        match_toggle_frame.pack(side=tk.LEFT, expand=True)
        tk.Label(match_toggle_frame, text="Match",
                 font=('Arial', 10)).pack(side=tk.TOP)
        self.match_toggle = RoundToggleButton(
            match_toggle_frame, command=self.toggle_match_highlight)
        self.match_toggle.pack(side=tk.TOP, pady=2)

        # Sync initial toggle values with the grid (if available)
        main_window = self.parent.winfo_toplevel().window
        if hasattr(main_window, 'grid'):
            grid = main_window.grid
            self.row_toggle.set_state(grid.show_row, trigger_command=False)
            self.column_toggle.set_state(
                grid.show_column, trigger_command=False)
            self.box_toggle.set_state(grid.show_box, trigger_command=False)
            self.match_toggle.set_state(
                grid.show_matching, trigger_command=False)

        # --- Main control row for New Game, Clear Board, and Comments indicator ---
        controls_frame = tk.Frame(self.frame)
        controls_frame.pack(fill='x')

        # New Game button
        ttk.Button(
            controls_frame,
            text="New Game",
            style='Rounded.TButton',
            command=self.back_to_difficulty
        ).pack(side=tk.LEFT, padx=5, expand=True)

        # Clear Board button
        ttk.Button(
            controls_frame,
            text="Clear Board",
            style='Rounded.TButton',
            command=self.clear_board
        ).pack(side=tk.LEFT, padx=5, expand=True)

        # Comments mode indicator with label
        self.comments_frame = tk.Frame(controls_frame)
        self.comments_frame.pack(side=tk.LEFT, padx=5, expand=True)

        tk.Label(
            self.comments_frame,
            text="Comments Mode (press 'c')",
            font=('Arial', 10)
        ).pack(side=tk.TOP)
        self.comments_indicator = tk.Label(
            self.comments_frame,
            text="OFF",
            font=('Arial', 10, 'bold'),
            fg='white',
            bg=COLORS['toggle_inactive'],
            width=6,
            padx=5,
            pady=2,
            relief='solid',
            borderwidth=1
        )
        self.comments_indicator.pack(side=tk.TOP, pady=2)

        # Save reference to control panel in main window for easy access
        main_window = self.parent.winfo_toplevel()
        if hasattr(main_window, 'window'):
            main_window.window.control_panel = self

    def update_comments_indicator(self, is_active):
        """Update the comments mode indicator appearance"""
        print(
            f"Control panel updating indicator to: {is_active}")  # Debug print

        # Use the same colors as the toggle button
        if is_active:
            self.comments_indicator.config(
                text="ON",
                # Use the same blue as toggle button
                bg=COLORS['toggle_active'],
                fg='white'
            )
        else:
            self.comments_indicator.config(
                text="OFF",
                # Use the same gray as toggle button
                bg=COLORS['toggle_inactive'],
                fg='white'
            )

        # Force the indicator to update immediately
        self.comments_indicator.update_idletasks()
        print("Indicator updated")  # Debug print

    def toggle_row_highlight(self):
        new_state = self.row_toggle.active
        main_window = self.parent.winfo_toplevel().window
        if hasattr(main_window, 'grid'):
            grid = main_window.grid
            grid.show_row = new_state
            if grid.selected_cell:
                row, col = grid.selected_cell
                grid.highlight_cell(row, col)

    def toggle_column_highlight(self):
        new_state = self.column_toggle.active
        main_window = self.parent.winfo_toplevel().window
        if hasattr(main_window, 'grid'):
            grid = main_window.grid
            grid.show_column = new_state
            if grid.selected_cell:
                row, col = grid.selected_cell
                grid.highlight_cell(row, col)

    def toggle_box_highlight(self):
        new_state = self.box_toggle.active
        main_window = self.parent.winfo_toplevel().window
        if hasattr(main_window, 'grid'):
            grid = main_window.grid
            grid.show_box = new_state
            if grid.selected_cell:
                row, col = grid.selected_cell
                grid.highlight_cell(row, col)

    def toggle_match_highlight(self):
        new_state = self.match_toggle.active
        main_window = self.parent.winfo_toplevel().window
        if hasattr(main_window, 'grid'):
            grid = main_window.grid
            grid.show_matching = new_state
            if grid.selected_cell:
                row, col = grid.selected_cell
                grid.highlight_cell(row, col)

    def back_to_difficulty(self):
        window = self.parent.winfo_toplevel()

        # Reset grid state if it exists
        if hasattr(window.window, 'grid'):
            window.window.grid.lives = 3
            window.window.grid.comments_mode = False
            window.window.grid.selected_cell = None
            # Unbind lingering events
            window.window.grid.frame.unbind('<Key>')
            window.window.grid.frame.unbind('<FocusOut>')

        # Destroy child windows (game-over dialogs, etc.)
        for child in window.winfo_children():
            if isinstance(child, tk.Toplevel):
                child.destroy()

        # Clear the main frame widgets
        for widget in self.parent.winfo_children():
            widget.destroy()

        if hasattr(window.window, 'grid'):
            delattr(window.window, 'grid')

        window.after(100, window.window.show_difficulty_selection)

    def clear_board(self):
        window = self.parent.winfo_toplevel()
        if hasattr(window.window, 'grid'):
            window.window.grid.clear_board()

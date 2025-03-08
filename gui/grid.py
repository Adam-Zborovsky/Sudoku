import tkinter as tk
from tkinter import ttk
from constants.settings import COLORS
import math
from gui.widgets.toggle_button import RoundToggleButton
from gui.widgets.sudoku_cell import SudokuCell


class RoundToggleButton(tk.Canvas):
    def __init__(self, parent, width=60, height=30, padding=3, command=None):
        super().__init__(parent, width=width, height=height,
                         bg=COLORS['white'], highlightthickness=0)
        self.command = command
        self.active = False  # Start inactive
        self.width = width
        self.height = height
        self.padding = padding

        # Animation settings
        self.animation_duration = 250  # Slightly faster animation
        self.animation_steps = 25
        self.animation_running = False

        # Calculate dimensions
        self.rail_height = height - 2*padding
        self.rail_radius = self.rail_height // 2
        self.circle_diameter = self.rail_height - 6  # Make circle slightly smaller

        # Create the background rail (pill shape)
        self.create_rail()

        # Initial circle position
        circle_y = self.height//2  # Center circle vertically
        shadow_offset = 2

        # Set initial position to the left (inactive state)
        initial_x = self.padding + 4

        self.circle_shadow = self.create_oval(
            initial_x-shadow_offset, circle_y-self.circle_diameter//2-shadow_offset,
            initial_x+self.circle_diameter+shadow_offset, circle_y +
            self.circle_diameter//2+shadow_offset,
            fill='#cccccc', outline='', tags='shadow'
        )
        self.circle = self.create_oval(
            initial_x, circle_y-self.circle_diameter//2,
            initial_x+self.circle_diameter, circle_y+self.circle_diameter//2,
            fill='white', outline='#e0e0e0', width=1,
            tags='circle'
        )

        # Ensure proper stacking order
        self.tag_raise('shadow')
        self.tag_raise('circle')

        # Set initial rail color
        self.itemconfig('rail', fill=COLORS['toggle_inactive'])

        self.bind('<Button-1>', self.toggle)

    def create_rail(self):
        # Create the rail background with true rounded corners using arcs
        x1, y1 = self.padding, self.padding
        x2, y2 = self.width - self.padding, self.height - self.padding
        radius = self.rail_radius

        # Create the base shape
        self.create_rectangle(
            x1 + radius, y1,
            x2 - radius, y2,
            fill=COLORS['toggle_active'], outline='',
            tags='rail'
        )

        # Add the rounded ends
        self.create_arc(
            x1, y1,
            x1 + 2*radius, y2,
            start=90, extent=180,
            fill=COLORS['toggle_active'], outline='',
            tags='rail'
        )
        self.create_arc(
            x2 - 2*radius, y1,
            x2, y2,
            start=-90, extent=180,
            fill=COLORS['toggle_active'], outline='',
            tags='rail'
        )

    def animate_toggle(self, start_x, end_x, step=0):
        if step <= self.animation_steps:
            # Enhanced easing function for more pronounced animation
            progress = step / self.animation_steps
            # Elastic ease-out for more bounce
            if progress < 0.5:
                fraction = 4 * progress * progress * progress
            else:
                p = progress - 1
                fraction = 1 + 4 * p * p * p + \
                    math.sin(progress * 4) * 0.1  # Add slight bounce

            current_x = start_x + (end_x - start_x) * fraction

            # Update circle and shadow position
            circle_y = self.height//2
            shadow_offset = 2

            # Update shadow position
            self.coords(self.circle_shadow,
                        current_x-shadow_offset, circle_y-self.circle_diameter//2-shadow_offset,
                        current_x+self.circle_diameter+shadow_offset, circle_y+self.circle_diameter//2+shadow_offset)

            # Update circle position
            self.coords(self.circle,
                        current_x, circle_y-self.circle_diameter//2,
                        current_x+self.circle_diameter, circle_y+self.circle_diameter//2)

            # Interpolate colors with slight bounce effect
            if self.active:
                color = COLORS['toggle_active']
            else:
                color = COLORS['toggle_inactive']

            # Update all rail parts
            self.itemconfig('rail', fill=color)

            # Schedule next animation frame
            self.after(self.animation_duration // self.animation_steps,
                       lambda: self.animate_toggle(start_x, end_x, step + 1))
        else:
            self.animation_running = False
            if self.command:
                self.command()

    def toggle(self, event=None):
        if self.animation_running:
            return

        self.animation_running = True
        self.active = not self.active

        if self.active:
            # Animate right
            start_x = self.padding + 4
            end_x = self.width - self.padding - self.circle_diameter - 4
        else:
            # Animate left
            start_x = self.width - self.padding - self.circle_diameter - 4
            end_x = self.padding + 4

        # Update rail color immediately
        self.itemconfig(
            'rail', fill=COLORS['toggle_active'] if self.active else COLORS['toggle_inactive'])
        self.animate_toggle(start_x, end_x)

        # Call the command after toggling state
        if self.command:
            self.command()

    def set_state(self, active):
        if active != self.active:
            self.active = active
            # Update the rail color immediately
            self.itemconfig(
                'rail', fill=COLORS['toggle_active'] if active else COLORS['toggle_inactive'])
            # Move circle to correct position without animation
            circle_y = self.height//2
            x = self.width - self.padding - self.circle_diameter - \
                4 if active else self.padding + 4
            shadow_offset = 2
            self.coords(self.circle_shadow,
                        x-shadow_offset, circle_y-self.circle_diameter//2-shadow_offset,
                        x+self.circle_diameter+shadow_offset, circle_y+self.circle_diameter//2+shadow_offset)
            self.coords(self.circle,
                        x, circle_y-self.circle_diameter//2,
                        x+self.circle_diameter, circle_y+self.circle_diameter//2)

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)


class SudokuCell(tk.Canvas):
    def __init__(self, parent, row, col, **kwargs):
        super().__init__(parent, width=60, height=60,
                         bg=COLORS['white'], highlightthickness=1, **kwargs)
        self.row = row
        self.col = col
        self.value = ""
        self.comments = set()  # Store comments as a set of numbers
        self.readonly = False
        self.bg_color = COLORS['white']
        self.size = 60  # Store size for matching outline drawing
        self.matching_outline = None  # Initialize matching outline

        # Fixed positions for each number 1-9 in a 3x3 grid
        self.comment_positions = {
            1: (15, 15),   # Top-left
            2: (30, 15),   # Top-middle
            3: (45, 15),   # Top-right
            4: (15, 30),   # Middle-left
            5: (30, 30),   # Center
            6: (45, 30),   # Middle-right
            7: (15, 45),   # Bottom-left
            8: (30, 45),   # Bottom-middle
            9: (45, 45)    # Bottom-right
        }

        # Create text items for main value and comments
        # Center the main value text
        self.value_text = self.create_text(
            30, 30,  # Center of the 60x60 cell
            text="",
            font=('Arial', 24),  # Larger font for main value
            fill='black',
            anchor='center'  # Ensure text is centered
        )
        self.comment_texts = {}  # Dictionary to store comment text items

    def set_value(self, value):
        self.value = str(value) if value else ""
        self.itemconfig(self.value_text, text=str(value) if value else "")
        if value:
            self.clear_comments()

    def add_comment(self, number):
        if not self.value and not self.readonly:  # Only add comments to empty, non-readonly cells
            if number in self.comments:
                self.remove_comment(number)
            else:
                self.comments.add(number)
                x, y = self.comment_positions[number]
                self.comment_texts[number] = self.create_text(
                    x, y,
                    text=str(number),
                    font=('Arial', 11),  # Slightly smaller for better fit
                    fill='gray40',
                    anchor='center'
                )
                # Raise comment text above background but below value text
                self.tag_lower(self.comment_texts[number], self.value_text)

    def remove_comment(self, number):
        if number in self.comments:
            self.comments.remove(number)
            if number in self.comment_texts:
                self.delete(self.comment_texts[number])
                del self.comment_texts[number]

    def clear_comments(self):
        for item in self.comment_texts.values():
            self.delete(item)
        self.comment_texts.clear()
        self.comments.clear()

    def refresh_comments(self):
        # Clear existing comment texts
        for item in self.comment_texts.values():
            self.delete(item)
        self.comment_texts.clear()

        # Recreate all comment texts in their fixed positions
        for number in self.comments:
            x, y = self.comment_positions[number]
            self.comment_texts[number] = self.create_text(
                x, y,
                text=str(number),
                font=('Arial', 12),
                fill='gray40',
                anchor='center'
            )

    def set_readonly(self, readonly):
        self.readonly = readonly
        self.bg_color = COLORS['readonly'] if readonly else COLORS['white']
        self.configure(bg=self.bg_color)

    def set_highlight(self, color):
        self.bg_color = color
        self.configure(bg=color)

    def get_highlight(self):
        return self.bg_color

    def add_matching_outline(self, color):
        """Draw a colored outline inside the cell boundaries for matching cells."""
        self.remove_matching_outline()
        # Draw an inner rectangle so the original border remains visible.
        self.matching_outline = self.create_rectangle(
            2, 2, self.size - 2, self.size - 2, outline=color, width=3)

    def remove_matching_outline(self):
        """Remove the matching outline if it exists."""
        if self.matching_outline is not None:
            self.delete(self.matching_outline)
            self.matching_outline = None


class SudokuGrid:
    def __init__(self, parent, game_logic):
        self.frame = tk.Frame(parent, bg=COLORS['white'])
        self.game_logic = game_logic
        self.cells = {}
        self.selected_cell = None
        self.comments_mode = False
        self.lives = 3  # Initialize with 3 lives
        self.parent = parent  # Store parent reference
        self.game_over_active = False  # flag to prevent multiple popups

        # Create the grid
        self.create_grid()

        # Create lives display
        self.lives_label = tk.Label(
            self.frame,
            text="❤️" * self.lives,
            font=('Arial', 16),
            bg=COLORS['white']
        )
        self.lives_label.grid(row=9, column=0, columnspan=9, pady=(5, 0))

        # Bind keyboard events to the frame
        self.frame.bind('<Key>', self.on_key_press)
        self.frame.configure(takefocus=1)
        self.frame.bind('<FocusOut>', lambda e: self.frame.focus_set())

        self.frame.pack(padx=10, pady=10)
        self.frame.focus_set()

        # Highlight flags
        self.show_row = True
        self.show_column = True
        self.show_box = False  # Box highlighting off by default
        self.show_matching = True  # Same-number highlight on by default

    def create_grid(self):
        # Create 9x9 grid of custom cells
        for i in range(9):
            self.frame.grid_rowconfigure(i, weight=1)
            self.frame.grid_columnconfigure(i, weight=1)
            for j in range(9):
                cell = SudokuCell(
                    self.frame,
                    row=i,
                    col=j
                )
                cell.grid(row=i, column=j, sticky='nsew',
                          # Slightly larger padding
                          padx=(2 if j % 3 != 2 else 3),
                          # Slightly larger padding
                          pady=(2 if i % 3 != 2 else 3))

                # Bind events
                cell.bind('<Button-1>', lambda e, r=i,
                          c=j: self.cell_clicked(r, c))

                self.cells[(i, j)] = cell

        # Add thicker borders for 3x3 boxes
        for i in range(3):
            for j in range(3):
                box_frame = tk.Frame(
                    self.frame,
                    borderwidth=2,
                    relief='solid'
                )
                box_frame.grid(
                    row=i*3, column=j*3,
                    rowspan=3, columnspan=3,
                    sticky='nsew'
                )
                box_frame.lower()

    def handle_keypress(self, event, row, col):
        if self.selected_cell is None:
            return "break"

        cell = self.cells[self.selected_cell]
        if cell.readonly:
            return "break"

        if event.char in '123456789':
            number = int(event.char)
            if self.comments_mode:
                # In comment mode, just toggle the comment number
                if number in cell.comments:
                    cell.remove_comment(number)
                else:
                    cell.add_comment(number)
            else:
                # In normal mode, try to set the value and check if it's correct
                cell.set_value(number)
                if self.game_logic.validate_move(row, col, number):
                    cell.set_highlight(COLORS['correct'])
                    cell.set_readonly(True)
                    self.clear_related_comments(row, col, number)
                else:
                    # Wrong answer handling - only in normal mode
                    self.lives -= 1
                    self.lives_label.config(text="❤️" * self.lives)
                    cell.set_highlight(COLORS['wrong'])
                    cell.set_value("")  # Clear the wrong value

                    if self.lives <= 0:
                        self.handle_game_over()
        elif event.keysym in ['BackSpace', 'Delete']:
            if not self.comments_mode:
                cell.set_value("")
                cell.set_highlight(COLORS['white'])
            else:
                cell.clear_comments()

        return "break"

    def clear_related_comments(self, row, col, number):
        # Clear comments with the same number in the same row
        for j in range(9):
            if j != col:
                self.cells[(row, j)].remove_comment(number)

        # Clear comments with the same number in the same column
        for i in range(9):
            if i != row:
                self.cells[(i, col)].remove_comment(number)

        # Clear comments with the same number in the same 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i, j) != (row, col):
                    self.cells[(i, j)].remove_comment(number)

    def set_comments_mode(self, enabled):
        """Set the comments mode state and update visual feedback."""
        print(f"Setting comments mode to: {enabled}")  # Debug print
        self.comments_mode = enabled

        # Get the main window
        main_window = self.parent.winfo_toplevel()
        print(f"Main window: {main_window}")  # Debug print

        # Look for control panel directly on the window instance
        if hasattr(main_window, 'window') and hasattr(main_window.window, 'control_panel'):
            print("Found control panel, updating indicator...")  # Debug print
            main_window.window.control_panel.update_comments_indicator(enabled)
        else:
            print("Could not find control panel")  # Debug print

        # Update cell highlighting if needed
        if self.selected_cell:
            row, col = self.selected_cell
            self.highlight_cell(row, col)

    def fill_grid(self, puzzle):
        for i in range(9):
            for j in range(9):
                value = puzzle[i][j]
                if value != 0:  # 0 represents empty cells
                    cell = self.cells[(i, j)]
                    cell.set_value(str(value))
                    cell.set_readonly(True)

    def cell_clicked(self, row, col):
        self.selected_cell = (row, col)
        self.highlight_cell(row, col)
        # Ensure frame has focus when cell is clicked
        self.frame.focus_set()

    def highlight_cell(self, row, col):
        # First, store which cells were correct (green)
        correct_cells = []
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                if cell.get_highlight() == COLORS['correct']:
                    correct_cells.append((i, j))

        # Clear all highlights and restore cell backgrounds based on readonly state.
        for i in range(9):
            for j in range(9):
                cell = self.cells[(i, j)]
                if cell.readonly and (i, j) not in correct_cells:
                    cell.set_highlight(COLORS['readonly'])
                else:
                    cell.set_highlight(COLORS['white'])

        # Highlight row
        if self.show_row:
            for j in range(9):
                cell = self.cells[(row, j)]
                if cell.readonly and (row, j) not in correct_cells:
                    cell.set_highlight(COLORS['readonly_row'])
                else:
                    cell.set_highlight(COLORS['row'])

        # Highlight column
        if self.show_column:
            for i in range(9):
                cell = self.cells[(i, col)]
                if cell.readonly and (i, col) not in correct_cells:
                    cell.set_highlight(COLORS['readonly_column'])
                else:
                    cell.set_highlight(COLORS['column'])

        # Highlight 3x3 box if enabled
        if self.show_box:
            box_row, box_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    cell = self.cells[(i, j)]
                    if cell.readonly and (i, j) not in correct_cells:
                        cell.set_highlight(COLORS['readonly_box'])
                    else:
                        cell.set_highlight(COLORS['box'])

        # Highlight the selected cell
        selected_cell = self.cells[(row, col)]
        if selected_cell.readonly and (row, col) not in correct_cells:
            selected_cell.set_highlight(COLORS['readonly_selected'])
        else:
            selected_cell.set_highlight(COLORS['selected'])

        # Restore correct (green) cells that aren't in highlighted groups.
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i, j in correct_cells:
            if not ((i == row and self.show_row) or
                    (j == col and self.show_column) or
                    (box_row <= i < box_row + 3 and box_col <= j < box_col + 3 and self.show_box)):
                self.cells[(i, j)].set_highlight(COLORS['correct'])

        # Highlight matching cells and cells with matching comments
        if self.show_matching and selected_cell.value:
            value_to_match = str(selected_cell.value)
            for (i, j), cell in self.cells.items():
                if (i, j) != (row, col):
                    if str(cell.value) == value_to_match:
                        cell.set_highlight(COLORS['matching'])
                    elif int(value_to_match) in cell.comments:
                        cell.set_highlight(COLORS['matching'])

    def on_key_press(self, event):
        if event.char.lower() == 'c':
            self.toggle_comment_mode_keyboard(event)
            return "break"

        if self.selected_cell is not None:
            row, col = self.selected_cell
            return self.handle_keypress(event, row, col)

        return "break"

    def clear_selected(self):
        if self.selected_cell is not None:
            cell = self.cells[self.selected_cell]
            if not cell.readonly:
                if self.comments_mode:
                    cell.clear_comments()
                else:
                    cell.set_value("")
                    cell.set_highlight(COLORS['white'])

    # Added clear_board method to clear all non-readonly cells
    def clear_board(self):
        for cell in self.cells.values():
            if not cell.readonly:
                cell.set_value("")
                cell.clear_comments()

    def handle_game_over(self):
        # If already showing a game–over window, do nothing
        if self.game_over_active:
            return
        self.game_over_active = True

        # Unbind key events so that further input does not trigger conflicting actions
        self.frame.unbind("<Key>")
        self.frame.unbind("<FocusOut>")

        # Get the main window reference (which is the toplevel of self.parent)
        main_window = self.parent.winfo_toplevel()

        # Create the game over dialog as a child of the main window
        game_over = tk.Toplevel(main_window)
        game_over.title("Game Over")
        game_over.geometry("300x150")
        game_over.resizable(False, False)
        # Disable close (X) button
        game_over.protocol("WM_DELETE_WINDOW", lambda: None)

        # Center the game over window relative to the main window
        main_window.update_idletasks()
        game_over.update_idletasks()
        x = main_window.winfo_rootx() + (main_window.winfo_width() -
                                         game_over.winfo_width()) // 2
        y = main_window.winfo_rooty() + (main_window.winfo_height() -
                                         game_over.winfo_height()) // 2
        game_over.geometry(f"+{x}+{y}")

        # Add the game over message and button
        tk.Label(
            game_over,
            text="Game Over!\nYou ran out of lives!",
            font=("Arial", 14)
        ).pack(pady=20)
        ttk.Button(
            game_over,
            text="New Game",
            command=lambda: self.reset_game(game_over, main_window)
        ).pack(pady=5)

        # Make the game over dialog modal
        try:
            game_over.grab_set()
        except Exception as e:
            print("Error with grab_set:", e)
        game_over.focus_set()

    def reset_game(self, game_over, main_window):
        # Release the grab and destroy the game over window
        try:
            game_over.grab_release()
        except Exception as e:
            print("Error releasing grab:", e)
        game_over.destroy()
        self.game_over_active = False

        # Reset game state variables
        self.lives = 3
        self.comments_mode = False
        self.selected_cell = None

        # Schedule a return to the difficulty selection screen.
        # We now call the method on main_window.window (the SudokuWindow instance).
        main_window.after(100, main_window.window.show_difficulty_selection)

    def toggle_comment_mode_keyboard(self, event):
        """Handle keyboard shortcut 'c' to toggle comment mode."""
        print("Toggle comment mode keyboard triggered")  # Debug print
        new_state = not self.comments_mode
        print(f"New state will be: {new_state}")  # Debug print
        self.set_comments_mode(new_state)
        return "break"

    # Note: As the codebase grows, it is a good idea to refactor and split functionality into separate files.
    # For instance, separating UI components (like the RoundToggleButton and SudokuGrid) into their own modules
    # can improve readability and maintainability.

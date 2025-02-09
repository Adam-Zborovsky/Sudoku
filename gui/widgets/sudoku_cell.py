import tkinter as tk
from constants.settings import COLORS

class SudokuCell(tk.Canvas):
    def __init__(self, parent, row, col, **kwargs):
        super().__init__(parent, width=60, height=60, bg=COLORS['white'], highlightthickness=1, **kwargs)
        self.row = row
        self.col = col
        self.value = ""
        self.comments = set()  # Store comments as a set of numbers
        self.readonly = False
        self.bg_color = COLORS['white']
        
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
        self.value = value
        self.itemconfig(self.value_text, text=str(value) if value else "")
        if value:  # Clear comments when setting a value
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
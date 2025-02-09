import tkinter as tk
from tkinter import ttk
from constants.settings import COLORS

class ControlPanel:
    def __init__(self, parent, game_logic):
        self.frame = tk.Frame(parent)
        self.game_logic = game_logic
        self.parent = parent
        self.create_controls()
        self.frame.pack(pady=10)

    def create_controls(self):
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
        
        # Create indicator label with softer styling
        self.comments_indicator = tk.Label(
            self.comments_frame,
            text="OFF",
            font=('Arial', 10, 'bold'),
            fg='white',
            bg=COLORS['toggle_inactive'],  # Use the same gray as toggle button
            width=6,
            padx=5,
            pady=2,
            relief='solid',  # Changed from 'raised' to 'solid' for a softer look
            borderwidth=1
        )
        self.comments_indicator.pack(side=tk.TOP, pady=2)
        
        # Store reference to control panel in the main window
        main_window = self.parent.winfo_toplevel()
        if hasattr(main_window, 'window'):
            main_window.window.control_panel = self

    def update_comments_indicator(self, is_active):
        """Update the comments mode indicator appearance"""
        print(f"Control panel updating indicator to: {is_active}")  # Debug print
        
        # Use the same colors as the toggle button
        if is_active:
            self.comments_indicator.config(
                text="ON",
                bg=COLORS['toggle_active'],  # Use the same blue as toggle button
                fg='white'
            )
        else:
            self.comments_indicator.config(
                text="OFF",
                bg=COLORS['toggle_inactive'],  # Use the same gray as toggle button
                fg='white'
            )
        
        # Force the indicator to update immediately
        self.comments_indicator.update_idletasks()
        print("Indicator updated")  # Debug print

    def back_to_difficulty(self):
        window = self.parent.winfo_toplevel()
        
        # Reset game grid state if it exists
        if hasattr(window.window, 'grid'):
            window.window.grid.lives = 3
            window.window.grid.comments_mode = False
            window.window.grid.selected_cell = None
            # Unbind events to prevent any lingering callbacks
            window.window.grid.frame.unbind('<Key>')
            window.window.grid.frame.unbind('<FocusOut>')
        
        # Destroy all child windows first
        for child in window.winfo_children():
            if isinstance(child, tk.Toplevel):
                child.destroy()
                
        # Then destroy all widgets in the main frame
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # Clear any references
        if hasattr(window.window, 'grid'):
            delattr(window.window, 'grid')
            
        # Show difficulty selection after everything is cleaned up
        window.after(100, window.window.show_difficulty_selection)

    def clear_board(self):
        window = self.parent.winfo_toplevel()
        if hasattr(window.window, 'grid'):
            window.window.grid.clear_board() 
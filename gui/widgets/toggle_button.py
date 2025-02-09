import tkinter as tk
import math
from constants.settings import COLORS

class RoundToggleButton(tk.Canvas):
    def __init__(self, parent, width=60, height=30, padding=3, command=None):
        super().__init__(parent, width=width, height=height, bg=COLORS['white'], highlightthickness=0)
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
            initial_x+self.circle_diameter+shadow_offset, circle_y+self.circle_diameter//2+shadow_offset,
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
                fraction = 1 + 4 * p * p * p + math.sin(progress * 4) * 0.1  # Add slight bounce
                
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
            
            # Interpolate colors
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
        self.itemconfig('rail', fill=COLORS['toggle_active'] if self.active else COLORS['toggle_inactive'])
        self.animate_toggle(start_x, end_x)
        
        # Call the command after toggling state
        if self.command:
            self.command()

    def set_state(self, active, trigger_command=True):
        """Set the toggle state without animation"""
        if active != self.active:
            self.active = active
            # Update the rail color immediately
            self.itemconfig('rail', fill=COLORS['toggle_active'] if active else COLORS['toggle_inactive'])
            # Move circle to correct position without animation
            circle_y = self.height//2
            x = self.width - self.padding - self.circle_diameter - 4 if active else self.padding + 4
            shadow_offset = 2
            self.coords(self.circle_shadow,
                       x-shadow_offset, circle_y-self.circle_diameter//2-shadow_offset,
                       x+self.circle_diameter+shadow_offset, circle_y+self.circle_diameter//2+shadow_offset)
            self.coords(self.circle,
                       x, circle_y-self.circle_diameter//2,
                       x+self.circle_diameter, circle_y+self.circle_diameter//2)
            if trigger_command and self.command:
                self.command() 
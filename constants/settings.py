# Game settings and constants
WINDOW_SIZE = "600x900"
WINDOW_BG = "#f0f0f0"

COLORS = {
    'selected': '#e0e0ff',
    'matching': '#f0f0ff',
    'row': '#fff0e0',
    'column': '#e0fff0',
    'box': '#ffe0f0',
    'white': '#ffffff',
    'correct': '#e6ffe6',  # Light green for correct numbers
    'wrong': '#ffe6e6',    # Light red for wrong numbers
    'readonly': '#d3d3d3',  # Darker gray for readonly cells
    'readonly_row': '#e6d5c3',  # Grayed orange
    'readonly_column': '#c3e6c3',  # Grayed green
    'readonly_box': '#e6c3d5',  # Grayed pink
    'readonly_selected': '#c3c3e6',  # Grayed blue
    'toggle_active': '#4a90e2',  # Blue for active toggle
    'toggle_inactive': '#bdc3c7'  # Gray for inactive toggle
}

DIFFICULTY_LEVELS = {
    'Easy': 35,
    'Medium': 30,
    'Hard': 25,
    'Expert': 15
}

ANIMATION_SETTINGS = {
    'steps': 10,
    'speed': 20
} 
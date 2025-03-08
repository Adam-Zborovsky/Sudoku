# Sudoku Game

A GUI-based Sudoku game built with Python and Tkinter. This project generates puzzles dynamically, supports multiple difficulty levels, and includes features such as move validation, a built-in game timer, and game state storage.

## Overview

The Sudoku Game lets you play classic Sudoku puzzles with a modern interface. When you start a new game, a puzzle is generated on the fly using a backtracking algorithm. You can choose from various difficulty levels (Easy, Medium, Hard, Expert) to match your skill level.

Key features include:

- **Dynamic Puzzle Generation:** Uses a backtracking algorithm to generate complete solutions and then removes cells based on the selected difficulty.
- **Multiple Difficulty Levels:** Customize your challenge from Easy to Expert.
- **Interactive GUI:** Built with Tkinter to provide a smooth and interactive gaming experience.
- **Game Timer & Storage:** Tracks your play time and allows game state saving/loading.
- **Standalone Executable (via PyInstaller):** Package the game as a self-contained executable that runs on machines without Python installed.

## Installation

### Prerequisites

- Python 3.x installed on your system.
- Tkinter (usually bundled with Python).
- (Optional) PyInstaller for packaging the app into an executable.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/sudoku-game.git
   cd sudoku-game
   ```

2. **Set Up a Virtual Environment**

   Create and activate a virtual environment:

   - On Unix/MacOS:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Install Dependencies**

   If you plan to package the project as an executable, install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

## Running the Game

With your virtual environment activated, you can run the game using:

```bash
python main.py
```

A window will open, and you can choose a difficulty level to start playing.

## Packaging as an Executable

To distribute the game without requiring users to install Python:

1. **Build the Executable**

   From your project root, run:

   ```bash
   pyinstaller --onefile --windowed main.py
   ```

   - `--onefile` bundles everything into a single executable.
   - `--windowed` ensures no console window appears when running the app.

2. **Locate and Distribute**

   Once PyInstaller completes, find your executable in the `dist` folder. Share the `.exe` file with your friends—they won't need Python installed on their machines.

> **Note:**  
> If your game relies on external data files (e.g., images, config files), make sure to include them using the `--add-data` flag when packing with PyInstaller.

## Project Structure

Here's an overview of the project structure:

```
├── main.py                   # Entry point for the application
├── gui/
│   ├── base_window.py        # Main GUI window class (SudokuWindow)
│   └── grid.py               # Grid management and game over logic
├── game/
│   ├── sudoku.py             # Core game logic and state management
│   └── generator.py          # Puzzle generation algorithm
├── utils/
│   ├── timer.py              # Timer utility for tracking game duration
│   └── storage.py            # Saving/loading game state functionality
└── constants/
    └── settings.py           # Game settings and constants (colors, difficulty, etc.)
```

## Contributing

Contributions to enhance the game, fix bugs, or add new features are welcome. Please feel free to fork the repository and submit a pull request or open an issue for discussion.

## License

This project is licensed under the [MIT License](LICENSE).

---

Enjoy playing Sudoku and happy coding!

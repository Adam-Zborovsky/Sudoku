from gui.base_window import SudokuWindow
from game.sudoku import SudokuGame

def main():
    game = SudokuGame()
    window = SudokuWindow(game)
    window.run()

if __name__ == "__main__":
    main()

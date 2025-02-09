import json
import os

class GameStorage:
    def __init__(self, save_file="game_save.json"):
        self.save_file = save_file
        
    def save_game(self, game_state):
        """
        Save the current game state to a file
        """
        data = {
            'puzzle': game_state.puzzle,
            'solution': game_state.solution,
            'difficulty': game_state.current_difficulty,
            'elapsed_time': game_state.timer.elapsed_time
        }
        
        with open(self.save_file, 'w') as f:
            json.dump(data, f)
            
    def load_game(self):
        """
        Load a saved game state from file
        Returns None if no save file exists
        """
        if not os.path.exists(self.save_file):
            return None
            
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
            return data
        except:
            return None
            
    def clear_save(self):
        """
        Delete the save file if it exists
        """
        if os.path.exists(self.save_file):
            os.remove(self.save_file) 
import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        
    def start(self):
        self.start_time = time.time()
        self.running = True
        
    def stop(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False
        
    def get_time_string(self):
        if not self.running:
            return "00:00"
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        return f"{minutes:02d}:{seconds:02d}" 
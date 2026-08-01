

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.elapsed = 0.0
        self.running = False
        self.start()

    def start(self):
        self.elapsed = 0
        self.running = True

    def stop(self):
        self.running = False

    def get_time(self):
        return self.elapsed

    def update(self, dt):
        if self.running:
            self.elapsed += dt
            if self.elapsed >= self.duration:
                self.running = False
                return True
        return False

    def is_done(self):
        return not self.running and self.elapsed >= self.duration

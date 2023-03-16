import time

#not needed but good to have 
class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = None
        self.remaining_time = duration

    def start(self):
        if self.start_time is None:
            self.start_time = time.monotonic()
        else:
            self.start_time = time.monotonic() - self.remaining_time

    def pause(self):
        if self.start_time is not None:
            self.remaining_time = time.monotonic() - self.start_time
            self.start_time = None

    def resume(self):
        if self.start_time is None:
            self.start_time = time.monotonic() - self.remaining_time

    def reset(self):
        self.start_time = None
        self.remaining_time = self.duration

    def time_remaining(self):
        if self.start_time is None:
            return self.remaining_time
        else:
            elapsed_time = time.monotonic() - self.start_time
            remaining_time = self.duration - elapsed_time
            return max(0, remaining_time)

class ChessTimer:
    def __init__(self, initial_time):
        self.initial_time = initial_time
        self.time_left = [initial_time, initial_time]  # [white_time_left, black_time_left]
        print(self.time_left)
        self.current_player = 0  # 0 for white, 1 for black
        self.last_move_time = time.time()

    def switch_player(self):
        self.current_player = 1 - self.current_player
        print(self.current_player)
        self.last_move_time = time.time()
        print(self.last_move_time)


    def get_time_left(self):
        elapsed_time = time.time() - self.last_move_time
        self.time_left[self.current_player] -= elapsed_time
        self.last_move_time = time.time()
        return self.time_left[self.current_player]

    def is_time_up(self):
        return self.get_time_left() < 0
    


timer = ChessTimer(6)
timer.switch_player()
left=timer.get_time_left()

while left>0:
    timer.time_left[timer.current_player] = left - 1
    left=left-1
    timer.switch_player()
    print(timer.get_time_left())

#Timer(60)  # Create a timer with a duration of 60 seconds.
# timer.start()  # Start the timer.
# time.sleep(1)  # Wait 10 seconds.
# timer.pause()  # Pause the timer.
# time.sleep(1)  # Wait 5 seconds.
# timer.resume()  # Resume the timer.
# time.sleep(1)  # Wait 10 seconds.
# remaining_time = timer.time_remaining()  # Get the remaining time on the timer.
# print(f"Time remaining: {remaining_time} seconds")  # Print the remaining time.
import tkinter as tk
import time
import math
from pynput import keyboard
import pyautogui
import threading
import pickle

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speedrun Timer")
        self.root.configure(bg='#222222')

        # Initialize variables
        self.start_time = None
        self.timer_running = False
        self.attempts = 0
        self.current_time = 0

        # Load Saved Time
        try:
            with open('savefile.pkl', 'rb') as file:
                self.best_time = pickle.load(file)
                seconds = math.floor(self.best_time / 1000)
                ms = self.best_time % 1000
                self.best_time = f"{seconds}:{ms:03}"
        except:
            self.best_time = "N/A"

        # Create a label to display the timer
        self.attempts_label = tk.Label(root, text="Attempts: 0", font=("Helvetica", 18), bg='#222222', fg='white')
        self.best_label = tk.Label(root, text="Best: " + str(self.best_time), font=("Helvetica", 18), bg='#222222', fg='white')
        self.timer_label = tk.Label(root, text="00:000", font=("Helvetica", 48), bg='#222222', fg='white')
        self.attempts_label.pack(anchor="w", pady=0)
        self.best_label.pack(anchor="w", pady=0)
        self.timer_label.pack(anchor="w", pady=0)
        self.root.attributes('-topmost', True)

        self.listener_thread = threading.Thread(target=self.start_listener)
        self.listener_thread.daemon = True  # Allow the program to exit even if thread is running
        self.listener_thread.start()

    def start_listener(self):
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()

    def on_key_press(self, key):
        if not self.timer_running:
            self.start_timer()
        elif str(key) == "Key.shift":
            self.stop_timer()

    def start_timer(self):
        if not self.timer_running:
            self.timer_label.config(fg="white")
            self.start_time = int(round(time.time() * 1000))
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False
        if pyautogui.pixel(688,370) == (214, 214, 214) and self.current_time > 3800:
            self.attempts += 1
            self.attempts_label.config(text=f"Attempts: {self.attempts}")
            self.timer_label.config(fg="green")
            if self.best_time:
                self.best_time = min(self.best_time, self.current_time)
                with open('savefile.pkl', 'wb') as file:
                    pickle.dump(self.best_time, file)
            else:
                self.best_time = self.current_time
            seconds = math.floor(self.best_time / 1000)
            ms = self.best_time % 1000
            self.best_label.config(text=f"Best: {seconds}:{ms:03}")
        else:
            self.timer_label.config(fg="red")

    def update_timer(self):
        if self.timer_running:
            self.current_time = int(round(time.time() * 1000)) - self.start_time
            seconds = math.floor(self.current_time / 1000)
            ms = self.current_time % 1000
            time_str = f"{seconds}:{ms:03}"
            self.timer_label.config(text=time_str)
            self.root.after(1, self.update_timer)

app_root = tk.Tk()
app = TimerApp(app_root)
app_root.mainloop()
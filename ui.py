from tkinter import *
import time
from api_word import data_words

THEME_COLOR = '#ffffff'


class TypingSpeedInterface:
    def __init__(self) -> None:
        self.words = data_words
        self.current_word_index = 0
        self.start_time = None
        self.correct_words = 0
        self.time_limit = 30  # 30 seconds time limit
        self.timer_running = False

        self.window = Tk()
        self.window.title("Typing Speed Test")
        self.window.config(padx=60, pady=40, bg=THEME_COLOR)

        self.title_label = Label(text="Typing Speed Test", fg="black", font=("Arial", 20, "bold"), bg=THEME_COLOR)
        self.title_label.grid(row=0, column=1)

        self.words_label = Label(text=" ".join(self.words), fg="black", font=("Arial", 14), bg=THEME_COLOR)
        self.words_label.grid(row=1, column=1)

        self.input_entry = Entry(width=40)
        self.input_entry.grid(row=2, column=1)
        self.input_entry.bind("<KeyRelease>", self.check_typing)

        self.timer_label = Label(text=f"Time left: {self.time_limit}s", fg="red", font=("Arial", 14), bg=THEME_COLOR)
        self.timer_label.grid(row=3, column=1)

        self.result_label = Label(text="", fg="green", font=("Arial", 14), bg=THEME_COLOR)
        self.result_label.grid(row=4, column=1)

        self.retry_button = Button(text="Retry", command=self.reset_test, fg="white", bg="blue", font=("Arial", 14))
        self.retry_button.grid(row=5, column=1)
        self.retry_button.grid_remove()

        self.window.mainloop()

    def check_typing(self, event):
        if self.start_time is None:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

        current_input = self.input_entry.get().strip()

        if current_input == self.words[self.current_word_index]:
            self.correct_words += 1
            self.current_word_index += 1
            self.input_entry.delete(0, END)

            if self.current_word_index < len(self.words):
                self.words_label.config(text=" ".join(self.words[self.current_word_index:]))
            else:
                self.end_test()

    def update_timer(self):
        if self.timer_running:
            time_elapsed = time.time() - self.start_time
            time_left = self.time_limit - int(time_elapsed)

            if time_left > 0:
                self.timer_label.config(text=f"Time left: {time_left}s")
                self.window.after(1000, self.update_timer)
            else:
                self.end_test()

    def end_test(self):
        # Stop the timer
        self.timer_running = False

        total_time = time.time() - self.start_time
        if self.current_word_index == len(self.words):
            words_per_minute = (self.correct_words / total_time) * 60
        else:
            words_per_minute = (self.correct_words / self.time_limit) * 60
        self.result_label.config(text=f"Time's up! Your typing speed is {words_per_minute:.2f} WPM.")
        self.input_entry.config(state="disabled")
        self.retry_button.grid()

    def reset_test(self):
        self.words = data_words
        self.current_word_index = 0
        self.start_time = None
        self.correct_words = 0
        self.timer_running = False
        self.input_entry.config(state="normal")
        self.input_entry.delete(0, END)
        self.words_label.config(text=" ".join(self.words))
        self.result_label.config(text="")
        self.timer_label.config(text=f"Time left: {self.time_limit}s")
        self.retry_button.grid_remove()
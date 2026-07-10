import tkinter as tk
from logger import get_logger
logger = get_logger("Language Button")
from config import *

class LanguageButton:
    def __init__(self, parent, languages, x, y, default="LT", command=None):
        self.command = command
        self.languages = languages
        self.x, self.y = x, y

        self.index = self.languages.index(default) if default in self.languages else 0

        self.var = tk.StringVar(value=self.languages[self.index])

        self.button = tk.Button(
            parent,
            textvariable=self.var,
            command=self._on_click,
            bg=BLACK, fg=WHITE,
            font=(MAIN_FONT, 32),
            highlightthickness=2,
            highlightbackground=BLACK,
            activebackground=WHITE,
            activeforeground=BLACK,
            bd=0,
            anchor="center"
        )
        self.button.place(x=self.x, y=self.y, anchor="center")

    def _on_click(self):
        self.index = (self.index + 1) % len(self.languages)
        new_lang = self.languages[self.index]
        self.var.set(new_lang)

        logger.info(f"Language switched to {new_lang}")

        if self.command:
            self.command(new_lang)

    def get(self):
        return self.var.get()
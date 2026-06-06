import tkinter as tk
from logger import get_logger
logger = get_logger("Language Dropdown")
from config import *

class LanguageDropdown:
    def __init__(self, parent, languages, x, y, default="LT", command=None):

        self.command = command
        self.var = tk.StringVar(value=default)
        self.x, self.y = x, y

        self.dropdown = tk.OptionMenu(parent, self.var, *languages, command=self._on_select)
        self.dropdown.config(
            bg=BLACK, fg=WHITE,
            font=(MAIN_FONT, 32),
            highlightthickness=2,
            highlightbackground=BLACK,
            activebackground=BLACK,
            activeforeground=WHITE,
            indicatoron=0,
            bd=0,
            anchor="center"
        )
        self.dropdown["menu"].config(
            bg=BLACK,
            fg=WHITE,
            font=(MAIN_FONT, 16),
            activebackground=WHITE,
            activeforeground=BLACK,
            borderwidth=2,
            relief="solid"
        )

        self.dropdown.place(x=self.x, y=self.y, anchor="center")
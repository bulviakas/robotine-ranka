import tkinter as tk
from tkinter import ttk
from logger import get_logger
logger = get_logger("Language Dropdown")
from config import *

class LanguageDropdown:
    def __init__(self, parent, languages, x, y, default="LT", command=None):
        """
        Custom styled dropdown menu for choosing app language.
        Looks like a minimal black/white box with bold text.
        """
        self.command = command
        self.var = tk.StringVar(value=default)
        self.x, self.y = x, y

        self.dropdown = tk.OptionMenu(parent, self.var, *languages, command=self._on_select)
        self.dropdown.config(
            bg=BLACK, fg=WHITE,
            font=(MAIN_FONT, 32, "bold"),
            highlightthickness=2,
            highlightbackground=BLACK,
            activebackground=BLACK,
            activeforeground=WHITE,
            indicatoron=0,
            bd=0
        )
        self.dropdown["menu"].config(
            bg=BLACK,
            fg=WHITE,
            font=(MAIN_FONT, 16, "bold"),
            activebackground=WHITE,
            activeforeground=BLACK,
            borderwidth=2,
            relief="solid"
        )

        self.dropdown.place(x=self.x, y=self.y, anchor="center")

    def _on_select(self, lang):
        if self.command:
            self.command(lang)

    def get(self):
        """Return currently selected language."""
        return self.var.get()

    def set(self, lang):
        self.var.set(lang)
        if self.command:
            self.command(lang)

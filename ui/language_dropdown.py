import tkinter as tk
from tkinter import ttk
from logger import get_logger
logger = get_logger("Language Dropdown")

class LanguageDropdown:
    def __init__(self, parent, languages, default="LT", command=None):
        """
        A styled dropdown for choosing app language.
        """
        self.command = command

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Black.TCombobox",
            fieldbackground="black",
            background="black",
            foreground="white",
            arrowcolor="white"
        )
        style.map(
            "Black.TCombobox",
            fieldbackground=[("readonly", "black")],
            foreground=[("readonly", "white")],
            background=[("readonly", "black")]
        )

        self.var = tk.StringVar(value=default)

        self.dropdown = ttk.Combobox(
            parent,
            textvariable=self.var,
            values=languages,
            state="readonly",
            style="Black.TCombobox"
        )
        self.dropdown.place(relx=0.9, rely=0.05, anchor="center")

        self.dropdown.bind("<<ComboboxSelected>>", self._on_select)

    def _on_select(self, event):
        lang = self.var.get()
        logger.info(f"Requested language switch to {lang}")
        if self.command:
            self.command(lang)

    def get(self):
        """Return currently selected language."""
        return self.var.get()

    def set(self, lang):
        self.var.set(lang)
        if self.command:
            self.command(lang)

import tkinter as tk
from logger import get_logger
logger = get_logger("Language Dropdown")
from config import *

class LanguageDropdown:
    def __init__(self, parent, languages, x, y, default="LT", command=None):
        
        self.command = command
        self.languages = languages
        self.current = default
        self.x, self.y = x, y
        self.parent = parent
        self._popup = None

        self.button = tk.Button(
            parent,
            text=default,
            bg=BLACK, fg=WHITE,
            font=(MAIN_FONT, 32),
            highlightthickness=2,
            highlightbackground=BLACK,
            activebackground=WHITE,
            activeforeground=BLACK,
            bd=0,
            relief="flat",
            anchor="center",
            command=self._toggle_popup,
        )
        self.button.place(x=self.x, y=self.y, anchor="center")

    def _toggle_popup(self):
        if self._popup and self._popup.winfo_exists():
            self._close_popup()
        else:
            self._open_popup()

    def _open_popup(self):
        self._popup = tk.Toplevel(self.parent)
        self._popup.overrideredirect(True)
        self._popup.config(bg=BLACK)

        bx = self.button.winfo_rootx()
        by = self.button.winfo_rooty()
        bh = self.button.winfo_height()

        for i, lang in enumerate(self.languages):
            btn = tk.Button(
                self._popup,
                text=lang,
                bg=BLACK, fg=WHITE,
                font=(MAIN_FONT, 26),
                activebackground=WHITE,
                activeforeground=BLACK,
                bd=0,
                relief="flat",
                anchor="center",
                width=4,
                command=lambda l=lang: self._select(l),
            )
            btn.grid(row=i, column=0, sticky="ew", padx=2, pady=1)

        self._popup.geometry(f"+{bx}+{by + bh + 2}")

        # Close popup if user clicks outside
        self._popup.bind("<FocusOut>", lambda _: self._close_popup())
        self._popup.focus_set()

    def _select(self, lang):
        self.current = lang
        self.button.config(text=lang)
        self._close_popup()
        if self.command:
            self.command(lang)

    def _close_popup(self):
        if self._popup and self._popup.winfo_exists():
            self._popup.destroy()
        self._popup = None

    def _on_select(self, lang):
        if self.command:
            self.command(lang)

    def get(self):
        """Return currently selected language."""
        return self.current

    def set(self, lang):
        self.current = lang
        self.button.config(text=lang)
        if self.command:
            self.command(lang)

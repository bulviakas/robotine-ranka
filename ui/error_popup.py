import tkinter as tk

class ErrorPopup(tk.Toplevel):
    def __init__(self, parent, title, message, level="error"):
        super().__init__(parent)

        self.title(title)
        self.transient(parent)
        self.grab_set()

        bg = "#ffdddd" if level == "error" else "#fff4cc"

        self.configure(bg=bg)
        self.resizable(False, False)

        tk.Label(
            self,
            text=title,
            font=("Arial", 16, "bold"),
            bg=bg
        ).pack(padx=20, pady=(15, 5))

        tk.Label(
            self,
            text=message,
            wraplength=320,
            justify="left",
            bg=bg
        ).pack(padx=20, pady=10)

        tk.Button(
            self,
            text="OK",
            command=self.destroy
        ).pack(pady=(0, 15))

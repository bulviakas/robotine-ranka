import tkinter as tk

class ErrorPopup(tk.Toplevel):
    def __init__(self, parent, title, message, on_ack=None):
        super().__init__(parent)

        self.title(title)
        self.geometry("500x250")
        self.configure(bg="#2b0000")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()  # modal

        tk.Label(
            self,
            text="ERROR",
            font=("Arial", 26, "bold"),
            fg="red",
            bg="#2b0000"
        ).pack(pady=10)

        tk.Label(
            self,
            text=message,
            font=("Arial", 14),
            fg="white",
            bg="#2b0000",
            wraplength=450,
            justify="center"
        ).pack(pady=15)

        tk.Button(
            self,
            text="ACKNOWLEDGE",
            font=("Arial", 14, "bold"),
            bg="red",
            fg="white",
            width=18,
            command=lambda: self._ack(on_ack)
        ).pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", lambda: None)  # prevent close

    def _ack(self, callback):
        if callback:
            callback()
        self.destroy()

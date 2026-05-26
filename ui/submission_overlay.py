import tkinter as tk


class SubmissionOverlay(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg="#000000")
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.lift()

        canvas = tk.Canvas(self, bg="#000000", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_rectangle(0, 0, 9999, 9999, fill="#000000", stipple="gray50", outline="")

        self.update_idletasks()
        self.grab_set()

    def close(self):
        self.grab_release()
        self.destroy()

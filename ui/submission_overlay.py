import tkinter as tk


class SubmissionOverlay(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg="#000000")
        self.grab_set()

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{sw}x{sh}+0+0")

        canvas = tk.Canvas(self, width=sw, height=sh, bg="#000000", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        canvas.create_rectangle(0, 0, sw, sh, fill="#000000", stipple="gray50", outline="")

    def close(self):
        self.grab_release()
        self.destroy()

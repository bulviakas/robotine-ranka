import tkinter as tk

class ErrorPopup(tk.Toplevel):
    def __init__(self, parent, title, message, level="hard"):
        super().__init__(parent)

        self.parent = parent
        self.level = level

        # --- Fullscreen dark overlay ---
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 1)
        self.configure(bg="#000000")
        self.grab_set()

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{sw}x{sh}+0+0")

        # --- Colors ---
        if level == "hard":
            accent = "#b00020"   # red
            title_text = "ERROR"
        else:
            accent = "#e6a700"   # amber
            title_text = "WARNING"

        panel_bg = "#121212"
        border_outer = "#2a2a2a"

        # --- Canvas ---
        canvas = tk.Canvas(
            self,
            width=sw,
            height=sh,
            bg="#000000",
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)

        # --- Panel geometry ---
        pw, ph = 560, 340
        px = (sw - pw) // 2
        py = (sh - ph) // 2

        # --- Darkened background ---
        canvas.create_rectangle(
            0, 0, sw, sh,
            fill="#000000",
            stipple="gray50",
            outline=""
        )

        # --- Outer border ---
        canvas.create_rectangle(
            px - 6, py - 6,
            px + pw + 6, py + ph + 6,
            fill=border_outer,
            outline=""
        )

        # --- Main panel ---
        canvas.create_rectangle(
            px, py,
            px + pw, py + ph,
            fill=panel_bg,
            outline=""
        )

        # --- Accent header ---
        canvas.create_rectangle(
            px, py,
            px + pw, py + 64,
            fill=accent,
            outline=""
        )

        # --- Title ---
        canvas.create_text(
            px + pw // 2,
            py + 32,
            text=title_text,
            fill="white",
            font=("Arial", 24, "bold")
        )

        # --- Message ---
        canvas.create_text(
            px + pw // 2,
            py + 150,
            text=message,
            fill="white",
            width=pw - 80,
            font=("Arial", 15),
            justify="center"
        )

        # --- Button ---
        btn_w, btn_h = 220, 56
        btn_x = px + pw // 2
        btn_y = py + ph - 70

        btn_border = canvas.create_rectangle(
            btn_x - btn_w // 2 - 2,
            btn_y - btn_h // 2 - 2,
            btn_x + btn_w // 2 + 2,
            btn_y + btn_h // 2 + 2,
            fill="white",
            outline=""
        )

        btn_rect = canvas.create_rectangle(
            btn_x - btn_w // 2,
            btn_y - btn_h // 2,
            btn_x + btn_w // 2,
            btn_y + btn_h // 2,
            fill="#1e1e1e",
            outline=""
        )

        btn_text = canvas.create_text(
            btn_x,
            btn_y,
            text="OK",
            fill="white",
            font=("Arial", 14, "bold")
        )

        for item in (btn_border, btn_rect, btn_text):
            canvas.tag_bind(item, "<Button-1>", self.close)

    def close(self, event=None):
        self.grab_release()
        self.destroy()
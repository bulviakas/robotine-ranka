import tkinter as tk
from config import WHITE, BLACK

# TODO translate all popups

class ErrorPopup(tk.Toplevel):
    def __init__(self, app, message, *, level="hard", on_ok=None):
        super().__init__(app.root)

        self.app = app
        self.level = level
        self.on_ok = on_ok

        # Fullscreen dark overlay
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg="#000000")
        self.grab_set()

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{sw}x{sh}+0+0")

        if level == "hard":
            accent = "#b00020"
            title_text = "popup_tt_error"
        elif level == "soft":
            accent = "#e6a700"
            title_text = "popup_tt_warning"
        elif level == "incomplete":
            accent = "#580054"
            title_text = "popup_tt_incomplete"
        else:
            accent = "#005819"
            title_text = "popup_tt_passed"

        panel_bg = BLACK
        border_outer = "#2a2a2a"

        self.canvas = tk.Canvas(
            self,
            width=sw,
            height=sh,
            bg=BLACK,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        pw, ph = 560, 340
        px = (sw - pw) // 2
        py = (sh - ph) // 2
        
        # Fullscreen semi-transparent background
        self.canvas.create_rectangle(
            0, 0, sw, sh,
            fill=BLACK,
            stipple="gray25",
            outline="",
        )

        # Popup shadow
        self.canvas.create_rectangle(
            px + 8, py + 8,
            px + pw + 8, py + ph + 8,
            fill=BLACK,
            stipple="gray50",
            outline=""
        )

        # Block outline
        self.canvas.create_rectangle(
            px - 6, py - 6,
            px + pw + 6, py + ph + 6,
            fill=border_outer,
            outline=""
        )

        # Error block
        self.canvas.create_rectangle(
            px, py,
            px + pw, py + ph,
            fill=panel_bg,
            outline=""
        )

        # Title background
        self.canvas.create_rectangle(
            px, py,
            px + pw, py + 64,
            fill=accent,
            outline=""
        )

        # Title
        self.canvas.title = self.canvas.create_text(
            px + pw // 2,
            py + 32,
            text=title_text,
            fill=WHITE,
            font=("Arial", 24, "bold")
        )
        self.app.lang_manager.register_widget(self.canvas, title_text, item_id=self.canvas.title)

        # Message
        self.canvas.create_text(
            px + pw // 2,
            py + 150,
            text=message,
            fill=WHITE,
            width=pw - 80,
            font=("Arial", 15),
            justify="center"
        )

        # Button
        btn_w, btn_h = 220, 56
        btn_x = px + pw // 2
        btn_y = py + ph - 70

        btn_border = self.canvas.create_rectangle(
            btn_x - btn_w // 2 - 2,
            btn_y - btn_h // 2 - 2,
            btn_x + btn_w // 2 + 2,
            btn_y + btn_h // 2 + 2,
            fill=WHITE,
            outline=""
        )

        btn_rect = self.canvas.create_rectangle(
            btn_x - btn_w // 2,
            btn_y - btn_h // 2,
            btn_x + btn_w // 2,
            btn_y + btn_h // 2,
            fill="#1e1e1e",
            outline=""
        )

        btn_text = self.canvas.create_text(
            btn_x,
            btn_y,
            text="OK",
            fill=WHITE,
            font=("Arial", 14, "bold")
        )

        for item in (btn_border, btn_rect, btn_text):
            self.canvas.tag_bind(item, "<Button-1>", self.close)

    def close(self, event=None):

        self.app.lang_manager.unregister_widget(self.canvas)

        self.grab_release()
        self.destroy()

        if self.on_ok:
            self.on_ok()
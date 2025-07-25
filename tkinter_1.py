import os
if "DISPLAY" not in os.environ:   # needed when starting from cron/rc.local
    os.environ["DISPLAY"] = ":0"
import tkinter as tk
from PIL import Image, ImageTk
import cairosvg
import io, re
from pathlib import Path

# ASSET PATHS
RESTART_BUTTON_PATH = Path("assets/restart_btn.svg")
SUBMIT_BUTTON_PATH = Path("assets/submit_btn.svg")

# CONSTANTS
OVERLAP_FRAC        = 0.2
CMD_BAR_HEIGHT_FRAC = 1.7
TOP_PAD_FRAC        = 0.19
MID_PAD_FRAC        = 0.05   # vertical gap between cmd bar & button
BOT_PAD_FRAC        = 0.10
SIDE_GAP_FRAC       = 0.02   # side padding for menu
GAP_BETWEEN_BTNS    = 3

def svg_to_photo(svg_file: Path, colour: str, size_xy) -> ImageTk.PhotoImage:
    """Return a PhotoImage of the SVG filled with *colour* (stroke stays)."""
    txt = svg_file.read_text(encoding="utf-8")
    txt = re.sub(r'fill\s*:\s*#[0-9a-fA-F]{3,6}', f'fill:{colour}', txt)
    txt = re.sub(r'fill="[^"]+"',                 f'fill="{colour}"', txt, flags=re.I)
    png = cairosvg.svg2png(bytestring=txt.encode(),
                           output_width=size_xy[0], output_height=size_xy[1])
    return ImageTk.PhotoImage(Image.open(io.BytesIO(png)))

class PuzzleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.title("Puzzle Command Builder")

        self.self_w, self.self_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = tk.Canvas(self.root, width=self.self_w, height=self.self_h, bg = 'black')
        self.canvas.pack(fill="both", expand=True)

        # piece width so that 9pw + 2 gap covers screen (5 pieces + 4 gaps = 9 pw)
        self.gap = int(SIDE_GAP_FRAC * self.self_w)
        self.piece_w  = int((self.self_w - 2*self.gap) / 8)
        self.piece_h  = int(self.piece_w * 0.6)

        self.img_refs = []

        # Command bar
        cmd_y = cmd_y = int(TOP_PAD_FRAC * self.self_h)
        self.cmd = CommandLine(self.canvas, self.self_w//2, cmd_y,
                               self.piece_w, self.piece_h, n_slots=9,
                               overlap=OVERLAP_FRAC)

        # BUTTONS
        btn_w = 380
        btn_h = 51
        btn_top  = cmd_y + int(self.piece_h * CMD_BAR_HEIGHT_FRAC) + 8

        # "Pradeti is naujo" button
        btn_left_1 = self.self_w//2 - btn_w - GAP_BETWEEN_BTNS
        restart_img = svg_to_photo(RESTART_BUTTON_PATH, 'white', (btn_w, btn_h))
        self.img_refs.append(restart_img)
        self.restart_btn = self.canvas.create_image(btn_left_1, btn_top, image=restart_img, anchor='nw')
        self.canvas.create_text(btn_left_1 + btn_w * 0.55, btn_top + btn_h//2 - 3, text="IŠVALYTI", font=('Cascadia Code SemiBold', 18, 'bold'), fill='black')
        
        # "Vykdyti" button
        btn_left_2 = self.self_w//2 + GAP_BETWEEN_BTNS
        submit_img = svg_to_photo(SUBMIT_BUTTON_PATH, 'white', (btn_w, btn_h))
        self.img_refs.append(submit_img)
        self.submit_btn = self.canvas.create_image(btn_left_2, btn_top, image=submit_img, anchor='nw') # Good fonts: Cascadia Code SemiBold, Segoe UI Black
        self.canvas.create_text(btn_left_2 + btn_w * 0.45, btn_top + btn_h//2 - 3, text="PALEISTI", font=('Cascadia Code SemiBold', 18, 'bold'), fill='black')

        self.root.bind("<Escape>", lambda e: self.root.destroy())
    
    def run(self):
        self.root.mainloop()

class CommandLine():
    def __init__(self, canvas, canvas_x, y_top, piece_w, piece_h, n_slots, overlap):
        self.canvas, self.piece_w, self.piece_h = canvas, piece_w, piece_h
        self.slot_w  = int(piece_w * (1 - overlap))
        self.slots   = [None] * n_slots

        total_w = self.slot_w * n_slots + int(piece_w * overlap)
        x0, x1  = canvas_x - total_w // 2, canvas_x + total_w // 2
        y1      = y_top + int(piece_h * CMD_BAR_HEIGHT_FRAC)

        def round_rectangle(x1, y1, x2, y2, radius=100, **kwargs):
        
            points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
                    x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
                    x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]

            return canvas.create_polygon(points, **kwargs, smooth=True)
        
        self.cmd_border = round_rectangle(x0, y_top, x1, y1, fill="black", outline="white", width=3)
        self.x0, self.y_mid = x0, (y_top + y1) // 2

if __name__ == "__main__":
    PuzzleApp().run()
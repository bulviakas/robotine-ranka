import os
if "DISPLAY" not in os.environ:   # needed when starting from cron/rc.local
    os.environ["DISPLAY"] = ":0"
import tkinter as tk
from PIL import Image, ImageTk
#import cairosvg
import io, re
from pathlib import Path

# GEOMETRY CONSTANTS
OVERLAP_FRAC        = 0.2
CMD_BAR_HEIGHT_FRAC = 1.7
TOP_PAD_FRAC        = 0.19
MID_PAD_FRAC        = 0.05   # vertical gap between cmd bar & button
BOT_PAD_FRAC        = 0.10
SIDE_GAP_FRAC       = 0.02   # side padding for menu

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

        # Command bar
        cmd_y = cmd_y = int(TOP_PAD_FRAC * self.self_h)
        self.cmd = CommandLine(self.canvas, self.self_w//2, cmd_y,
                               self.piece_w, self.piece_h, n_slots=9,
                               overlap=OVERLAP_FRAC)

        # BUTTONS
        btn_w = int(2.5 * self.piece_w)
        btn_h = int(btn_w / 8)
        btn_top  = cmd_y + int(self.piece_h * CMD_BAR_HEIGHT_FRAC) + 8
        btn_bot  = btn_top + btn_h

        # "Pradeti is naujo" button
        btn_left_1 = self.self_w//2 - btn_w - 2
        btn_right_1= btn_left_1 + btn_w
        self.canvas.create_rectangle(btn_left_1, btn_top, btn_right_1, btn_bot,
                                     fill="white")
        
        # "Vykdyti" button
        btn_left_2 = self.self_w//2 + 2
        btn_right_2 = btn_left_2 + btn_w
        self.canvas.create_rectangle(btn_left_2, btn_top, btn_right_2, btn_bot, fill="white")

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
        
        cmd_border = round_rectangle(x0, y_top, x1, y1, fill="black", outline="white", width=3)
        self.x0, self.y_mid = x0, (y_top + y1) // 2

if __name__ == "__main__":
    PuzzleApp().run()
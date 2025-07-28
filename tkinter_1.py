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
START_BLOCK_PATH = Path("assets/start_block.svg")
CMD_BLOCK_PATH = Path("assets/game_blocks.svg")

# CONSTANTS
OVERLAP_FRAC        = 0.2
CMD_BAR_HEIGHT_FRAC = 1.7
TOP_PAD_FRAC        = 0.19
MID_PAD_FRAC        = 0.05   # vertical gap between cmd bar & button
BOT_PAD_FRAC        = 0.10
SIDE_GAP_FRAC       = 0.02   # side padding for menu
GAP_BETWEEN_BTNS    = 3
BLOCK_SIZE_COEF     = 0.85
CMD_SIDE_PAD        = 32
CMD_H_PAD           = 16

MENU_COLOURS = [
    "#e74c3c", "#f39c12", "#27ae60", "#8e44ad", "#96d5ff",
    "#ff5f7f", "#f1c40f", "#2980b9"   # 8 pieces
]

BLOCK_LABELS = [
    "NAMŲ\nPOZICIJA", "SILPNAS\nPAKRATYMAS", "STIPRUS\nPAKRATYMAS", "ŠALDYTUVO\nPOZICIJA",
    "SKENAVIMO\nPOZICIJA", "TRUMPA\nPAUZĖ", "ILGESNĖ\nPAUZĖ", "GALUTINĖ\nPOZICIJA"
]

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
        self.piece_w  = 165 * BLOCK_SIZE_COEF
        self.piece_h  = 85 * BLOCK_SIZE_COEF

        self.img_refs = []

        # Command bar
        cmd_y = cmd_y = int(TOP_PAD_FRAC * self.self_h)
        self.cmd = CommandLine(self.canvas, self.self_w//2, cmd_y,
                               self.piece_w, self.piece_h, n_slots=9,
                               overlap=OVERLAP_FRAC)

        # BUTTONS
        btn_w = 380
        btn_h = 51
        btn_top  = cmd_y + CMD_H_PAD + int(self.piece_h * CMD_BAR_HEIGHT_FRAC) + 8

        # "Pradeti is naujo" button
        btn_left_1 = self.self_w//2 - btn_w - GAP_BETWEEN_BTNS
        restart_img = svg_to_photo(RESTART_BUTTON_PATH, 'white', (btn_w, btn_h))
        self.img_refs.append(restart_img)
        self.restart_btn = self.canvas.create_image(btn_left_1, btn_top, image=restart_img, anchor='nw')
        self.canvas.create_text(btn_left_1 + btn_w * 0.55, btn_top + btn_h//2 - 3, 
                                text="IŠVALYTI", font=('Cascadia Code SemiBold', 18, 'bold'), fill='black')
        
        # "Vykdyti" button
        btn_left_2 = self.self_w//2 + GAP_BETWEEN_BTNS
        submit_img = svg_to_photo(SUBMIT_BUTTON_PATH, 'white', (btn_w, btn_h))
        self.img_refs.append(submit_img)
        self.submit_btn = self.canvas.create_image(btn_left_2, btn_top, image=submit_img, anchor='nw') # Good fonts: Cascadia Code SemiBold, Segoe UI Black
        self.canvas.create_text(btn_left_2 + btn_w * 0.45, btn_top + btn_h//2 - 3, 
                                text="PALEISTI", font=('Cascadia Code SemiBold', 18, 'bold'), fill='black')

        # Start block
        start_block = Block(self, 'white', self.cmd.x0 + self.piece_w//2, 
                            cmd_y + self.cmd.piece_h//2 + CMD_H_PAD, template=False, start=True,
                            text="PRADŽIA", text_offset=0)
        self.cmd.try_snap(start_block)
        start_block.lock()

        # --- Menu grid positions (4 per row) ---
        first_row_y  = (self.self_h - (btn_top + btn_h))//2 + btn_top + btn_h - self.piece_h
        second_row_y = first_row_y + self.piece_h + self.piece_h
        row_centres  = [first_row_y, second_row_y]

        # x positions for 4 centres: gap + piece_w/2 + col*2piece_w
        x0 = self.self_w//2 - 3 * self.piece_w
        col_x = [x0 + c * 2*self.piece_w for c in range(4)]

        # Create 10 template pieces
        for idx, colour in enumerate(MENU_COLOURS):
            row, col = divmod(idx, 4)
            label = BLOCK_LABELS[idx]
            Block(self, colour, col_x[col], row_centres[row], template=True, text=label)

        self.root.bind("<Escape>", lambda e: self.root.destroy())
    
    def run(self):
        self.root.mainloop()

# TODO fix the command line placement (last block goes over the outline)

class CommandLine():
    def __init__(self, canvas, canvas_x, y_top, piece_w, piece_h, n_slots, overlap):
        self.canvas, self.piece_w, self.piece_h = canvas, piece_w, piece_h
        self.slot_w  = int(piece_w * (1 - overlap))
        self.slots   = [None] * n_slots

        total_w = self.slot_w * n_slots # + int(piece_w * overlap)
        x0, x1  = canvas_x - total_w // 2, canvas_x + total_w // 2
        y1      = y_top + int(piece_h * CMD_BAR_HEIGHT_FRAC)

        def round_rectangle(x1, y1, x2, y2, radius=100, **kwargs):
        
            points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
                    x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
                    x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]

            return canvas.create_polygon(points, **kwargs, smooth=True)
        
        self.cmd_border = round_rectangle(x0 - CMD_SIDE_PAD, y_top - CMD_H_PAD, 
                                          x1 + CMD_SIDE_PAD, y1 + CMD_H_PAD, fill="black", 
                                          outline="white", width=3)
        self.x0, self.y_mid = x0, (y_top + y1) // 2

    def release(self, block):
        if block.slot is not None and not block.locked:
            self.slots[block.slot] = None
            block.slot = None

    def try_snap(self, block):
        bb = self.canvas.bbox(block.tag)
        if not bb:
            return False
        cx = (bb[0] + bb[2]) / 2
        slot = int((cx - self.x0) // self.slot_w)

        # validity: in range & sequential
        if not (0 <= slot < len(self.slots)):     return False
        if self.slots[slot] is not None:          return False
        if slot and self.slots[slot-1] is None:   return False

        # snap!
        tgt_cx = self.x0 + slot*self.slot_w + self.piece_w//2
        dx, dy = tgt_cx - cx, self.y_mid - ((bb[1]+bb[3]) / 2)
        self.canvas.move(block.tag, dx, dy)
        self.slots[slot], block.slot = block, slot
        print("SNAP!")
        return True

class Block():
    def __init__(self, app, colour, x, y, template=False, start=False, text="", text_offset=7):
        self.app, self.canvas = app, app.canvas
        self.colour, self.template = colour, template
        self.home_x, self.home_y   = x, y
        self.slot = None
        self.locked = False
        self.text = text
        self.tag = f"block_{id(self)}"
        
        if start:
            img = svg_to_photo(START_BLOCK_PATH, colour, (app.piece_w, app.piece_h))
        else:
            img = svg_to_photo(CMD_BLOCK_PATH, colour, (app.piece_w, app.piece_h))
        app.img_refs.append(img)
        self.item = self.canvas.create_image(x, y, image=img, anchor="center", tags=self.tag)
        self.label = self.canvas.create_text(x + text_offset, y, text=text, 
                                             font=('Cascadia Code SemiBold', 10, 'bold'), 
                                             fill='black', anchor='center', tags=self.tag, justify='center')

        for ev, cb in (("<Button-1>", self.on_click),
                       ("<B1-Motion>", self.on_drag),
                       ("<ButtonRelease-1>", self.on_release)):
            self.canvas.tag_bind(self.tag, ev, cb)

    # TODO fix clone spawning (either spawn a claw right after start or spawn and drag on one click)

    def on_click(self, ev):
        if not self.locked:
            self.app.cmd.release(self)
            if self.template:
                # spawn a draggable clone
                clone = Block(self.app, self.colour, self.home_x, self.home_y, template=False, text=self.text)
                clone.on_click(ev)
                return
            self.drag_x, self.drag_y = ev.x, ev.y

    def on_drag(self, ev):
        if not self.locked:
            if self.template: return
            dx, dy = ev.x - self.drag_x, ev.y - self.drag_y
            self.canvas.move(self.tag, dx, dy)
            self.drag_x, self.drag_y = ev.x, ev.y

    def on_release(self, _ev):
        if not self.locked:
            if self.template: return
            if not self.app.cmd.try_snap(self):
                self.return_home()

    def return_home(self):
        cx, cy = [(bb[0]+bb[2])/2 for bb in (self.canvas.bbox(self.tag),)][0], \
                 [(bb[1]+bb[3])/2 for bb in (self.canvas.bbox(self.tag),)][0]
        self.canvas.move(self.tag, self.home_x - cx, self.home_y - cy)
        self.slot = None

    def lock(self):
        self.locked = True
        print("Block locked")

if __name__ == "__main__":
    PuzzleApp().run()
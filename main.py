import os
if "DISPLAY" not in os.environ:   # needed when starting from cron/rc.local
    os.environ["DISPLAY"] = ":0"
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import cairosvg
import io, re
from pathlib import Path
import cv2

# ASSET PATHS
RESTART_BUTTON_PATH = Path("assets/restart_btn.svg")
SUBMIT_BUTTON_PATH = Path("assets/submit_btn.svg")
START_BLOCK_PATH = Path("assets/start_block.svg")
CMD_BLOCK_PATH = Path("assets/game_blocks.svg")
BLOCK_TEMPLATE_PATH = Path("assets/block_template.svg")
CMD_BLOCK_PATH = Path("assets/cmd_block.svg")
TT_ICON_PATH = Path("assets/tutorial_icon_thin.svg")
HOME_ICON_PATH = Path("assets/home_icon_thin.svg")
LNG_ICON_PATH = Path("assets/language_icon_thin.svg")
START_BTN_PATH = Path("assets/start_btn.svg")
CONTEXT_VIDEO_PATH = Path("assets/Fish-spinning.mp4")
INSTRUCTIONS_VIDEO_PATH = Path("assets/roach.gif")

# CONSTANTS
OVERLAP_FRAC        = 0.2
CMD_BAR_HEIGHT_FRAC = 1.7
TOP_PAD_FRAC        = 0.19
MID_PAD_FRAC        = 0.05   # vertical gap between cmd bar & button
BOT_PAD_FRAC        = 0.1
SIDE_GAP_FRAC       = 0.02   # side padding for menu
GAP_BETWEEN_BTNS    = 3
BLOCK_SIZE_COEF     = 0.02
CMD_SIDE_PAD        = 32
CMD_H_PAD           = 16
MENU_TOP_FRAC       = 0.08

# TODO: import better fonts

# Good fonts: Cascadia Code SemiBold, Segoe UI Black
MAIN_FONT = "Cascadia Code SemiBold"

BLOCK_COLOURS = [
    "#e74c3c", "#f39c12", "#27ae60", "#8e44ad", "#96d5ff",
    "#ff5f7f", "#f1c40f", "#2980b9"   # 8 pieces
]

BLOCK_LABELS = [
    "TESTAVIMO\nPOZICIJA", "SILPNAS\nPAKRATYMAS", "STIPRUS\nPAKRATYMAS", "ŠALDYTUVO\nPOZICIJA",
    "SKENAVIMO\nPOZICIJA", "TRUMPA\nPAUZĖ", "ILGA\nPAUZĖ", "GALUTINĖ\nPOZICIJA"
]

THE_CORRECT_SEQUENCE = [
    "ŠALDYTUVO\nPOZICIJA", "TESTAVIMO\nPOZICIJA", "STIPRUS\nPAKRATYMAS", "SKENAVIMO\nPOZICIJA",
    "ILGA\nPAUZĖ", "TESTAVIMO\nPOZICIJA", "GALUTINĖ\nPOZICIJA", None
]

CONTEXT_VIDEO_SIZE = [480, 854] # Change when importing the actual video
INSTRUCTIONS_VIDEO_SIZE = [360, 480]

CONTEXT_TEXT = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed faucibus at sapien ac egestas. "
    "Morbi quis tellus ut mauris efficitur pellentesque ac luctus nisl. Pellentesque pharetra sapien dui. "
    "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. "
    "Vivamus a tortor nec elit auctor sagittis eu at risus. Nulla ut ex eu justo luctus blandit ac non ipsum. "
    "Mauris sollicitudin fringilla eros, ac vulputate orci sagittis non. "
    "Donec a tortor vestibulum, blandit enim quis, convallis dolor. Curabitur laoreet justo quis rutrum pellentesque. "
    "Curabitur nisi ex, ornare eu blandit at, pulvinar eu eros. Proin sollicitudin massa sed nibh sollicitudin bibendum. "
)

def svg_to_coloured_photo(svg_file: Path, colour: str, size_xy, mirror=False) -> ImageTk.PhotoImage:
    """Return a PhotoImage of the SVG filled with *colour* (stroke stays)."""
    txt = svg_file.read_text(encoding="utf-8")
    txt = re.sub(r'fill\s*:\s*#[0-9a-fA-F]{3,6}', f'fill:{colour}', txt)
    txt = re.sub(r'fill="[^"]+"',                 f'fill="{colour}"', txt, flags=re.I)
    png = cairosvg.svg2png(bytestring=txt.encode(),
                           output_width=size_xy[0], output_height=size_xy[1])
    pil_img = Image.open(io.BytesIO(png)).convert("RGBA")

    if mirror:
        pil_img = ImageOps.mirror(pil_img)

    return ImageTk.PhotoImage(pil_img)

def svg_to_photo(svg_path, width=None, height=None):

    svg_path = str(svg_path)
    png_bytes = cairosvg.svg2png(url=svg_path, output_width=width, output_height=height)
    image = Image.open(io.BytesIO(png_bytes))

    return ImageTk.PhotoImage(image)

class PuzzleApp:
    def __init__(self):
        global BLOCK_SIZE_COEF
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.title("Puzzle Command Builder")

        self.self_w, self.self_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

        # piece width so that 9pw + 2 gap covers screen (5 pieces + 4 gaps = 9 pw)
        self.gap = int(SIDE_GAP_FRAC * self.self_w)
        self.piece_h  = self.self_h//8
        self.piece_w  = 165 * (self.piece_h / 85)
        BLOCK_SIZE_COEF = self.piece_h / 85
        if self.piece_w > self.self_w//9:
            self.piece_w = self.self_w//9
            self.piece_h = 85 * (self.piece_w / 165)
            BLOCK_SIZE_COEF = self.piece_w / 165

        self.img_refs = []

        # FIXME change the pure black to a different shade

        # Create container frame to hold pages
        self.container = tk.Frame(self.root, bg='black')
        self.container.pack(fill="both", expand=True)

        # Pages
        self.start_page = tk.Frame(self.container, bg='black')
        self.game_page = tk.Frame(self.container, bg='black')
        self.context_page = tk.Frame(self.container, bg='black')
        self.instructions_page = tk.Frame(self.container, bg='black')

        self.start_page.place(relwidth=1, relheight=1)
        self.game_page.place(relwidth=1, relheight=1)
        self.context_page.place(relwidth=1, relheight=1)
        self.instructions_page.place(relwidth=1, relheight=1)

        # --- PAGE SETUP ---

        # FIXME: Change the random labels to actually meaningful text

        def setup_start_page(self):
            canvas = tk.Canvas(self.start_page, width=self.self_w, height=self.self_h, bg='black', highlightthickness=0)
            canvas.pack()

            title = tk.Label(self.start_page, text="Kazkoks inviting sukis or whatever!!!", font=(MAIN_FONT, int(44 * (self.self_h / 5 / 165))), fg="white", bg="black")
            title.place(relx=0.5, rely=0.35, anchor='center')

            start_tag = 'start'
            start_img = svg_to_coloured_photo(START_BTN_PATH, BLOCK_COLOURS[2], (self.self_w / 2, self.self_h / 5))
            self.img_refs.append(start_img)
            start_btn = canvas.create_image(int(self.self_w * 0.5), int(self.self_h * 0.6), image=start_img, anchor='center', tags=start_tag)
            canvas.tag_bind(start_tag, "<Button-1>", lambda e: self.show_page(self.context_page))

            canvas.create_text(int(self.self_w * 0.5), int(self.self_h * 0.595), text="ŽAISTI", font=(MAIN_FONT, int(48 * (self.self_h / 5 / 165)), 'bold'), fill='black', tags=start_tag)

        def setup_context_page(self):
            canvas = tk.Canvas(self.context_page, width=self.self_w, height=self.self_h, bg='black', highlightthickness=0)
            canvas.pack()

            self.context_video_frame = tk.Frame(self.context_page, bg='black')
            self.context_video_frame.place(relx=0.5, rely=0.425, anchor='center')

            # NEXT Button
            self.next_tag = 'next'
            next_img = svg_to_coloured_photo(CMD_BLOCK_PATH, BLOCK_COLOURS[6], (1.25*self.piece_w, 1.25*self.piece_h))
            self.img_refs.append(next_img)
            self.next_btn = canvas.create_image(int(self.self_w * 0.9), int(self.self_h * 0.9), image=next_img, anchor='center', tags=self.next_tag)
            canvas.create_text(int(self.self_w * 0.9) + 7, int(self.self_h * 0.9), 
                                    text="TOLIAU", font=(MAIN_FONT, int(18 * BLOCK_SIZE_COEF), 'bold'), fill='black', tags=self.next_tag)
            canvas.tag_bind(self.next_tag, "<Button-1>", lambda e: self.show_page(self.instructions_page))

            # Video block
            video_h = self.self_h * 0.75
            video_w = CONTEXT_VIDEO_SIZE[1] * (video_h / CONTEXT_VIDEO_SIZE[0])

            self.context_video = VideoPlayer(
                self.context_video_frame,
                video_path=CONTEXT_VIDEO_PATH,
                width=int(video_w),
                height=int(video_h)
            )

            self.context_video.label.pack()

        def setup_instructions_page(self):
            canvas = tk.Canvas(self.instructions_page, width=self.self_w, height=self.self_h, bg='black', highlightthickness=0)
            canvas.pack()

            # BACK Button
            self.back_tag = 'back'
            back_img = svg_to_coloured_photo(CMD_BLOCK_PATH, BLOCK_COLOURS[5], (1.25*self.piece_w, 1.25*self.piece_h), mirror=True)
            self.img_refs.append(back_img)
            back_btn = canvas.create_image(int(self.self_w * 0.1), int(self.self_h * 0.9), image=back_img, tags=self.back_tag)
            canvas.create_text(int(self.self_w * 0.1 - 7), int(self.self_h * 0.9), 
                                    text="ATGAL", font=(MAIN_FONT, int(18 * BLOCK_SIZE_COEF), 'bold'), fill='black', tags=self.back_tag)
            canvas.tag_bind(self.back_tag, "<Button-1>", lambda e: self.show_page(self.context_page))

            # PLAY Button
            self.play_tag = 'play'
            play_img = svg_to_coloured_photo(CMD_BLOCK_PATH, BLOCK_COLOURS[6], (1.25*self.piece_w, 1.25*self.piece_h))
            self.img_refs.append(play_img)
            self.next_btn = canvas.create_image(int(self.self_w * 0.9), int(self.self_h * 0.9), image=play_img, anchor='center', tags=self.play_tag)
            canvas.create_text(int(self.self_w * 0.9) + 7, int(self.self_h * 0.9), 
                                    text="TOLIAU", font=(MAIN_FONT, int(18 * BLOCK_SIZE_COEF), 'bold'), fill='black', tags=self.play_tag)
            canvas.tag_bind(self.play_tag, "<Button-1>", lambda e: self.show_page(self.game_page))

            # FIXME change the relative placement so that the video with the text would be centered

            # Video block
            video_h = self.self_h * 0.65
            video_w = INSTRUCTIONS_VIDEO_SIZE[1] * (video_h / INSTRUCTIONS_VIDEO_SIZE[0])
            if video_w > (self.self_w * 1.6 / 3):
                video_w = self.self_w * 1.6 / 3
                video_h = INSTRUCTIONS_VIDEO_SIZE[0] * (video_w / INSTRUCTIONS_VIDEO_SIZE[1])

            self.instructions_video_frame = tk.Frame(self.instructions_page, bg='white')
            self.instructions_video_frame.place(relx=0.3, rely=0.425, anchor='center')
            
            self.instructions_video = VideoPlayer(
                self.instructions_video_frame,
                video_path=INSTRUCTIONS_VIDEO_PATH,
                width=int(video_w),
                height=int(video_h)
            )

            self.instructions_video.label.pack()

            # TEXT BLOCK
            canvas.text_block = canvas.create_text(
                int(self.self_w * 0.3 + video_w / 2 + 32), 
                int(self.self_h * 0.425), 
                anchor="w", 
                fill='white', 
                font=(MAIN_FONT, 14), 
                text=CONTEXT_TEXT, 
                width=video_w / 1.5
                )

        def setup_game_page(self):
            self.canvas = tk.Canvas(self.game_page, width=self.self_w, height=self.self_h, bg='black', highlightthickness=0)
            self.canvas.pack(fill="both", expand=True)

            # Command bar
            cmd_y = int(TOP_PAD_FRAC * self.self_h)
            self.cmd = CommandLine(self, self.canvas, self.self_w//2, cmd_y,
                                self.piece_w, self.piece_h, n_slots=9,
                                overlap=OVERLAP_FRAC)
            
            # TODO: rewrite all button actions on left mouse click release and add "animations"

            # BUTTONS w:380 h:51
            btn_h = (CMD_H_PAD + int(self.piece_h * CMD_BAR_HEIGHT_FRAC)) // 3
            btn_w = 380 * (btn_h / 51)
            btn_top  = cmd_y + CMD_H_PAD + int(self.piece_h * CMD_BAR_HEIGHT_FRAC) + 8

            # CLEAR button
            self.clear_tag = 'clear'
            btn_left_1 = self.self_w//2 - btn_w - GAP_BETWEEN_BTNS
            clear_img = svg_to_coloured_photo(RESTART_BUTTON_PATH, 'white', (btn_w, btn_h))
            self.img_refs.append(clear_img)
            self.clear_btn = self.canvas.create_image(btn_left_1, btn_top, image=clear_img, anchor='nw', tags=self.clear_tag)
            self.canvas.create_text(btn_left_1 + btn_w * 0.55, btn_top + btn_h//2 - 3, 
                                    text="IŠVALYTI", font=(MAIN_FONT, int(18 * (btn_h / 51)), 'bold'), fill='black', tags=self.clear_tag)
            self.canvas.tag_bind(self.clear_tag, "<Button-1>", self.cmd.clear)

            # SUBMIT button
            self.submit_tag = 'submit'
            btn_left_2 = self.self_w//2 + GAP_BETWEEN_BTNS
            submit_img = svg_to_coloured_photo(SUBMIT_BUTTON_PATH, 'white', (btn_w, btn_h))
            self.img_refs.append(submit_img)
            self.submit_btn = self.canvas.create_image(btn_left_2, btn_top, image=submit_img, anchor='nw', tags=self.submit_tag) 
            self.canvas.create_text(btn_left_2 + btn_w * 0.45, btn_top + btn_h//2 - 3, 
                                    text="PALEISTI", font=(MAIN_FONT, int(18 * (btn_h / 51)), 'bold'), fill='black', tags=self.submit_tag)
            self.canvas.tag_bind(self.submit_tag, "<Button-1>", self.cmd.submit)

            # ICONS ---
            icon_size = self.self_h * TOP_PAD_FRAC // 2.75

            # TUTORIAL icon
            self.tt_tag = 'tutorial'
            tt_y = self.self_h * MENU_TOP_FRAC
            tt_x = (self.self_w - self.cmd.x1) / 2 + self.cmd.x1
            tt_img = svg_to_coloured_photo(TT_ICON_PATH, 'white', (icon_size, icon_size))
            self.img_refs.append(tt_img)
            self.tt_icon = self.canvas.create_image(tt_x, tt_y, image=tt_img, anchor='center', tags=self.tt_tag)
            self.canvas.tag_bind(self.tt_tag, "<Button-1>", lambda e: self.show_page(self.context_page))

            # HOME icon
            self.home_tag = 'home'
            home_y = self.self_h * MENU_TOP_FRAC
            home_x = self.cmd.x0 // 2
            home_img = svg_to_coloured_photo(HOME_ICON_PATH, 'white', (icon_size, icon_size))
            self.img_refs.append(home_img)
            self.tt_icon = self.canvas.create_image(home_x, home_y, image=home_img, anchor='center', tags=self.home_tag)
            self.canvas.tag_bind(self.home_tag, "<Button-1>", lambda e: self.show_page(self.start_page))

            # TODO: make a dropdown menu for changing languages (perhaps a seperate class)

            # LANGUAGE icon
            lng_y = self.self_h * MENU_TOP_FRAC
            lng_x = tt_x - 1.5*icon_size
            lng_img = svg_to_coloured_photo(LNG_ICON_PATH, 'white', (icon_size, icon_size))
            self.img_refs.append(lng_img)
            self.tt_icon = self.canvas.create_image(lng_x, lng_y, image=lng_img, anchor='center')

            # Start block
            start_block = Block(self, self.cmd, 'white', self.cmd.x0 + self.piece_w//2, 
                                cmd_y + self.cmd.piece_h//2 + CMD_H_PAD, template=False, start=True,
                                text="PRADŽIA", text_offset=0)
            self.cmd.try_snap(start_block)
            start_block.lock()

            # --- Menu grid positions (4 per row) ---
            first_row_y  = self.self_h//2 + (self.self_h//8)
            second_row_y = first_row_y + 1.5*self.self_h//8
            row_centres  = [first_row_y, second_row_y]

            # x positions for 4 centres: gap + piece_w/2 + col*2piece_w
            x0 = self.self_w//2 - 3 * self.piece_w
            col_x = [x0 + c * 2*self.piece_w for c in range(4)]

            # Create 10 template pieces
            for idx, colour in enumerate(BLOCK_COLOURS):
                row, col = divmod(idx, 4)
                label = BLOCK_LABELS[idx]
                Block(self, self.cmd, colour, col_x[col], row_centres[row], template=True, text=label)
            
        setup_start_page(self)
        setup_game_page(self)
        setup_context_page(self)
        setup_instructions_page(self)

        self.show_page(self.start_page)

        self.root.bind("<Escape>", lambda e: self.root.destroy())
    
    def run(self):
        self.root.mainloop()

    def show_page(self, page):
        """Raise the specified page to the front."""
        if page == self.context_page:
            self.context_video.start()
        else:
            self.context_video.stop()
        if page == self.instructions_page:
            self.instructions_video.start()
        else:
            self.instructions_video.stop()
        page.tkraise()

class CommandLine():
    def __init__(self, app, canvas, canvas_x, y_top, piece_w, piece_h, n_slots, overlap):
        self.canvas, self.piece_w, self.piece_h, self.app, self.n_slots = canvas, piece_w, piece_h, app, n_slots
        self.slot_w  = int(piece_w * (1 - overlap))
        self.slots   = [None] * self.n_slots

        total_w = self.slot_w * self.n_slots + int(piece_w * overlap)
        x0, self.x1  = canvas_x - total_w // 2, canvas_x + total_w // 2
        y1      = y_top + int(piece_h * CMD_BAR_HEIGHT_FRAC)
        self.x0, self.y_mid = x0, (y_top + y1) // 2

        def round_rectangle(x1, y1, x2, y2, radius=100, **kwargs):
        
            points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
                    x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
                    x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]

            return canvas.create_polygon(points, **kwargs, smooth=True)
        
        self.cmd_border = round_rectangle(x0 - CMD_SIDE_PAD, y_top - CMD_H_PAD, 
                                          self.x1 + CMD_SIDE_PAD, y1 + CMD_H_PAD, fill="black", 
                                          outline="white", width=3)
        
        self.cmd_img = svg_to_photo(CMD_BLOCK_PATH, self.piece_w, self.piece_h)
        app.img_refs.append(self.cmd_img)
        

    def release(self, block):
        if block.slot is not None and not block.locked:
            if self.slots[block.slot - 1] is not None:
                self.slots[block.slot - 1].unlock()
            self.canvas.delete(f"bg_{block.slot + 1}")
            self.slots[block.slot] = None
            block.slot = None

    def try_snap(self, block):
        bb = self.canvas.bbox(block.tag)
        if not bb:
            return False
        cx = (bb[0] + bb[2]) / 2
        cy = (bb[1] + bb[3]) / 2
        slot = int((cx - self.x0) // self.slot_w)

        # validity: in range & sequential
        if not (0 <= slot < len(self.slots)):     return False
        if self.slots[slot] is not None:          return False
        if slot and self.slots[slot-1] is None:   return False
        if abs(cy - self.y_mid) > 2*self.piece_h: 
            print("Too far away")
            return False

        # snap!
        tgt_cx = self.x0 + slot*self.slot_w + self.piece_w//2
        dx, dy = tgt_cx - cx, self.y_mid - ((bb[1]+bb[3]) / 2)
        self.canvas.move(block.tag, dx, dy)
        self.slots[slot], block.slot = block, slot
        print("SNAP!")
        if self.slots[block.slot - 1] is not None:
            self.slots[block.slot - 1].lock()
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        if slot + 1 < self.n_slots:
            self.canvas.create_image(tgt_cx + self.slot_w, self.y_mid, image=self.cmd_img, 
                                                            anchor="center", tags=f"bg_{slot + 1}")
        return True

    def clear(self, event):
        print("Clearing...")
        for slot, block in enumerate(self.slots):
            if block is None: 
                print("CLEARED!")
                return
            if block.text == "PRADŽIA": continue
            block.destroy()
            self.canvas.delete(f"bg_{slot + 1}")
            self.slots[slot] = None
            block.slot = None
            
        print("CLEARED!")
        return
    
    def submit(self, event):
        print("Submited!")
        print("-----------------")
        for block in self.slots:
            if block is None: 
                print("---------------")
                return
            print(block.text, "\n")
        print("-----------------")
        return



class Block():
    def __init__(self, app, cmd, colour, x, y, template=False, start=False, text="", text_offset=7):
        self.app, self.canvas = app, app.canvas
        self.colour, self.template = colour, template
        self.home_x, self.home_y   = x, y
        self.slot = None
        self.locked = False
        self.text, self.font_size = text, int(12 * BLOCK_SIZE_COEF)
        self.tag = f"block_{id(self)}"
        self.cmd = cmd
        self.text_offset = text_offset

        if start:
            img = svg_to_coloured_photo(START_BLOCK_PATH, colour, (app.piece_w, app.piece_h))
            self.font_size = int(14 * BLOCK_SIZE_COEF)
        elif self.template:
            img = svg_to_coloured_photo(BLOCK_TEMPLATE_PATH, colour, (1.5*app.piece_w, 1.5*app.piece_h))
            self.font_size = int(self.font_size * 1.5)
            self.text_offset = 2
        else:
            img = svg_to_coloured_photo(CMD_BLOCK_PATH, colour, (app.piece_w, app.piece_h))
        app.img_refs.append(img)
        self.item = self.canvas.create_image(x, y, image=img, anchor="center", tags=self.tag)
        self.label = self.canvas.create_text(x + self.text_offset, y, text=text, 
                                             font=(MAIN_FONT, self.font_size, 'bold'), 
                                             fill='black', anchor='center', tags=self.tag, justify='center')

        for ev, cb in (("<Button-1>", self.on_click),
                       ("<B1-Motion>", self.on_drag),
                       ("<ButtonRelease-1>", self.on_release)):
            self.canvas.tag_bind(self.tag, ev, cb)

    def on_click(self, ev):
        print("Block clicked")
        if not self.locked:
            self.app.cmd.release(self)
            if self.template:
                # spawn a draggable clone
                clone = Block(self.app, self.cmd, self.colour, ev.x, ev.y, template=False, text=self.text)

                clone.drag_x, clone.drag_y = ev.x, ev.y
                clone.on_drag(ev)

                def drag_handler(e): clone.on_drag(e)
                def release_handler(e): clone.on_release(e)

                canvas = self.canvas
                canvas.bind("<B1-Motion>", drag_handler)
                canvas.bind("<ButtonRelease-1>", release_handler)
                return
            self.drag_x, self.drag_y = ev.x, ev.y


    def on_drag(self, ev):
        if not self.locked:
            if self.template: return
            dx, dy = ev.x - self.drag_x, ev.y - self.drag_y
            self.canvas.move(self.tag, dx, dy)
            self.drag_x, self.drag_y = ev.x, ev.y

    def on_release(self, _ev):
        print("Block released")
        if not self.locked:
            if self.template: return
            if not self.app.cmd.try_snap(self):
                self.return_home()
                self.canvas.unbind("<B1-Motion>")
                self.canvas.unbind("<ButtonRelease-1>")

    def return_home(self):
        self.destroy()
        self.slot = None

    def lock(self):
        self.locked = True
        print(self.text, " block locked")
    
    def unlock(self):
        if self.text != "PRADŽIA":
            self.locked = False
            print(self.text, " block unlocked")

    def destroy(self):
        self.canvas.delete(self.tag)

class VideoPlayer:
    def __init__(self, parent, video_path, width=None, height=None):
        self.parent = parent
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.width = width
        self.height = height

        self.label = tk.Label(parent, bg='black')
        self.label.pack()

        self.playing = False

        # FIXME: make the video restart when the user enters the context page

    def start(self):
        if not self.playing:
            self.playing = True
            self._play_frame()

    def stop(self):
        self.playing = False

    def _play_frame(self):
        if not self.playing:
            return

        ret, frame = self.cap.read()
        if not ret:
            # Restart video
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
            if not ret:
                self.stop()
                return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Resize frame if needed
        if self.width and self.height:
            frame = cv2.resize(frame, (self.width, self.height))

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

        self.parent.after(33, self._play_frame) # ~30FPS (hopefully will be better)

    def destroy(self):
        self.stop()
        self.cap.release()
        self.label.destroy()

if __name__ == "__main__":
    PuzzleApp().run()
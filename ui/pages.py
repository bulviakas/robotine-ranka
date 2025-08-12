from config import *
from utils import load_svg_img
import tkinter as tk
from ui import VideoPlayer, CommandLine, Block
from logger import get_logger
logger = get_logger("Pages")

# FIXME: Change the random labels to actually meaningful text

def setup_start_page(self):

    logger.info("Setting up the Start page...")

    canvas = tk.Canvas(self.start_page, width=self.self_w, height=self.self_h, bg='black', highlightthickness=0)
    canvas.pack()

    title = tk.Label(self.start_page, text="Kazkoks inviting sukis or whatever!!!", font=(MAIN_FONT, int(44 * (self.self_h / 5 / 165))), fg="white", bg="black")
    title.place(relx=0.5, rely=0.35, anchor='center')

    start_tag = 'start'
    start_img = load_svg_img(self, START_BTN_PATH, (self.self_w / 2, self.self_h / 5), BLOCK_COLOURS[2])

    create_button(
        self, canvas, 
        img=start_img, 
        x=int(self.self_w * 0.5), y=int(self.self_h * 0.6), 
        text="ŽAISTI", 
        font_size=int(48 * (self.self_h / 5 / 165)), 
        tag=start_tag, 
        command=lambda e: self.show_page(self.context_page)
        )

def setup_context_page(self):

    logger.info("Setting up the Context page...")
    
    canvas = tk.Canvas(self.context_page, width=self.self_w, height=self.self_h, bg='black', highlightthickness=0)
    canvas.pack()

    self.context_video_frame = tk.Frame(self.context_page, bg='black')
    self.context_video_frame.place(relx=0.5, rely=0.425, anchor='center')

    # NEXT Button
    self.next_tag = 'next'
    next_img = load_svg_img(self, CMD_BLOCK_PATH, (1.25*self.piece_w, 1.25*self.piece_h), BLOCK_COLOURS[6])

    create_button(
        self, canvas,
        img=next_img,
        x=int(self.self_w * 0.9),
        y=int(self.self_h * 0.9),
        text="TOLIAU",
        font_size=int(18 * BLOCK_SIZE_COEF),
        tag=self.next_tag,
        command=lambda e: self.show_page(self.instructions_page),
        text_offset_x=7
    )

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

    logger.info("Setting up the Instructions page...")

    canvas = tk.Canvas(self.instructions_page, width=self.self_w, height=self.self_h, bg='black', highlightthickness=0)
    canvas.pack()

    # BACK Button
    self.back_tag = 'back'
    back_img = load_svg_img(self, CMD_BLOCK_PATH, (1.25*self.piece_w, 1.25*self.piece_h), BLOCK_COLOURS[5], mirror=True)

    create_button(
        self, canvas,
        img=back_img,
        x=int(self.self_w * 0.1), 
        y=int(self.self_h * 0.9),
        text="ATGAL",
        font_size=int(18 * BLOCK_SIZE_COEF),
        tag=self.back_tag,
        command=lambda e: self.show_page(self.context_page),
        text_offset_x=-7
    )

    # PLAY Button
    self.play_tag = 'play'
    play_img = load_svg_img(self, CMD_BLOCK_PATH, (1.25*self.piece_w, 1.25*self.piece_h), BLOCK_COLOURS[6])

    create_button(
        self, canvas,
        img=play_img,
        x=int(self.self_w * 0.9),
        y=int(self.self_h * 0.9),
        text="TOLIAU",
        font_size=int(18 * BLOCK_SIZE_COEF),
        tag=self.play_tag,
        command=lambda e: self.show_page(self.game_page),
        text_offset_x=7
    )

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

    logger.info("Setting up the Game page...")
    
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
    clear_img = load_svg_img(self, RESTART_BUTTON_PATH, (btn_w, btn_h), 'white')

    create_button(
        self, self.canvas,
        img=clear_img,
        x=btn_left_1 + btn_w / 2,
        y=btn_top + btn_h / 2,
        text="IŠVALYTI",
        font_size=int(18 * (btn_h / 51)),
        tag=self.clear_tag,
        command=self.cmd.clear,
        text_offset_x=btn_w * 0.05,
    )

    # SUBMIT button
    self.submit_tag = 'submit'
    btn_left_2 = self.self_w//2 + GAP_BETWEEN_BTNS
    submit_img = load_svg_img(self, SUBMIT_BUTTON_PATH, (btn_w, btn_h), 'white')
    self.submit_btn = self.canvas.create_image(btn_left_2, btn_top, image=submit_img, anchor='nw', tags=self.submit_tag) 
    self.canvas.create_text(btn_left_2 + btn_w * 0.45, btn_top + btn_h//2 - 3, 
                            text="PALEISTI", font=(MAIN_FONT, int(18 * (btn_h / 51)), 'bold'), fill='black', tags=self.submit_tag)
    self.canvas.tag_bind(self.submit_tag, "<Button-1>", self.cmd.submit)

    create_button(
        self, self.canvas,
        img=submit_img,
        x=btn_left_2 + btn_w * 0.5,
        y=btn_top + btn_h//2,
        text="PALEISTI",
        font_size=int(18 * (btn_h / 51)),
        tag=self.submit_tag,
        command=self.cmd.submit,
        text_offset_x=-btn_w * 0.05
    )

    # ICONS ---
    icon_size = self.self_h * TOP_PAD_FRAC // 2.75

    # TUTORIAL icon
    self.tt_tag = 'tutorial'
    tt_y = self.self_h * MENU_TOP_FRAC
    tt_x = (self.self_w - self.cmd.x1) / 2 + self.cmd.x1
    tt_img = load_svg_img(self, TT_ICON_PATH, (icon_size, icon_size), 'white')
    self.tt_icon = self.canvas.create_image(tt_x, tt_y, image=tt_img, anchor='center', tags=self.tt_tag)
    self.canvas.tag_bind(self.tt_tag, "<Button-1>", lambda e: self.show_page(self.context_page))

    # HOME icon
    self.home_tag = 'home'
    home_y = self.self_h * MENU_TOP_FRAC
    home_x = self.cmd.x0 // 2
    home_img = load_svg_img(self, HOME_ICON_PATH, (icon_size, icon_size), 'white')
    self.tt_icon = self.canvas.create_image(home_x, home_y, image=home_img, anchor='center', tags=self.home_tag)
    self.canvas.tag_bind(self.home_tag, "<Button-1>", lambda e: self.show_page(self.start_page))

    # TODO: make a dropdown menu for changing languages (perhaps a seperate class)

    # LANGUAGE icon
    lng_y = self.self_h * MENU_TOP_FRAC
    lng_x = tt_x - 1.5*icon_size
    lng_img = load_svg_img(self, LNG_ICON_PATH, (icon_size, icon_size), 'white')
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

def create_button(self, canvas, img, x, y, text, font_size, tag, command, text_offset_x=0, anchor="center"):
    canvas.create_image(x, y, image=img, tags=tag, anchor=anchor)
    canvas.create_text(x + text_offset_x, y, text=text, font=(MAIN_FONT, font_size, 'bold'), fill='black', tags=tag)
    canvas.tag_bind(tag, "<Button-1>", command)
import os
if "DISPLAY" not in os.environ:   # needed when starting from cron/rc.local
    os.environ["DISPLAY"] = ":0"
import tkinter as tk
from utils import svg_to_coloured_photo
from ui import VideoPlayer, Block, CommandLine
from config import *
import config

class PuzzleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.title("Puzzle Command Builder")

        self.self_w, self.self_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

        # piece width so that 9pw + 2 gap covers screen (5 pieces + 4 gaps = 9 pw)
        self.gap = int(SIDE_GAP_FRAC * self.self_w)
        self.piece_h  = self.self_h//8
        self.piece_w  = 165 * (self.piece_h / 85)
        config.BLOCK_SIZE_COEF = self.piece_h / 85
        if self.piece_w > self.self_w//9:
            self.piece_w = self.self_w//9
            self.piece_h = 85 * (self.piece_w / 165)
            config.BLOCK_SIZE_COEF = self.piece_w / 165

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

if __name__ == "__main__":
    PuzzleApp().run()

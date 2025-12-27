import os
if "DISPLAY" not in os.environ:   # needed when starting from cron/rc.local
    os.environ["DISPLAY"] = ":0"
import tkinter as tk
from config import *
import config
from ui.pages import *
from logger import get_logger
logger = get_logger("Main")
from language_manager import LanguageManager

class PuzzleApp:
    def __init__(self):
        logger.info("Initializing PuzzleApp...")
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        #self.root.geometry("800x480+0+0")
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after_idle(self.root.attributes, "-topmost", False)
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

        logger.debug(f"BLOCK_SIZE_COEF set to {config.BLOCK_SIZE_COEF:.3f}")

        self.img_refs = []

        # Create container frame to hold pages
        self.container = tk.Frame(self.root, bg=BLACK)
        self.container.pack(fill="both", expand=True)

        # Pages
        self.start_page = tk.Frame(self.container, bg=BLACK)
        self.game_page = tk.Frame(self.container, bg=BLACK)
        self.context_page = tk.Frame(self.container, bg=BLACK)
        self.instructions_page = tk.Frame(self.container, bg=BLACK)

        self.start_page.place(relwidth=1, relheight=1)
        self.game_page.place(relwidth=1, relheight=1)
        self.context_page.place(relwidth=1, relheight=1)
        self.instructions_page.place(relwidth=1, relheight=1)

        self.lang_manager = LanguageManager(self, default_lang="LT")
            
        setup_start_page(self)
        setup_game_page(self)
        setup_context_page(self)
        setup_instructions_page(self)

        self.show_page(self.start_page)

        logger.info("PuzzleApp setup complete.")

        self.root.bind("<Escape>", lambda e: self.root.destroy())
    
    def run(self):
        self.root.mainloop()

    def show_page(self, page):
        """Raise the specified page to the front."""
        if page == self.context_page:
            self.context_video.restart()
        else:
            self.context_video.stop()
        if page == self.instructions_page:
            self.instructions_video.restart()
        else:
            self.instructions_video.stop()
        if page == self.start_page:
            try:
                self.cmd.clear()
            except AttributeError:
                logger.warning("Game not setup yet, unable to clear")
                pass
        page.tkraise()
        logger.info(f"Switched to {page}")

if __name__ == "__main__":
    PuzzleApp().run()

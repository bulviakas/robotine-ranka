from config import *
import config
from utils import load_svg_img
from logger import get_logger
logger = get_logger("Block")

class Block():
    def __init__(self, app, cmd, colour, x, y, template=False, start=False, text="", text_offset=7):
        self.app, self.canvas = app, app.canvas
        self.colour, self.template = colour, template
        self.home_x, self.home_y   = x, y
        self.slot = None
        self.locked = False
        self.text, self.font_size = text, scale_font(12)
        self.tag = f"block_{id(self)}"
        self.cmd = cmd
        self.text_offset = text_offset

        if start:
            img = load_svg_img(app, START_BLOCK_PATH, (app.piece_w, app.piece_h), colour)
            self.font_size = scale_font(14)

        elif self.template:
            img = load_svg_img(app, BLOCK_TEMPLATE_PATH, (1.5*app.piece_w, 1.5*app.piece_h), colour)
            self.font_size = int(self.font_size * 1.5)
            self.text_offset = 2

        else:
            img = load_svg_img(app, CMD_BLOCK_PATH, (app.piece_w, app.piece_h), colour)

        self.item = self.canvas.create_image(
            x, y, 
            image=img, 
            anchor="center", 
            tags=self.tag
            )
        
        self.label = self.canvas.create_text(
            x + self.text_offset, y, 
            text=text.replace(' ', '\n'), 
            font=(MAIN_FONT, self.font_size, 'bold'), 
            fill=BLACK, 
            anchor='center', 
            tags=self.tag, 
            justify='center'
            )

        for ev, cb in (("<Button-1>", self.on_click),
                       ("<B1-Motion>", self.on_drag),
                       ("<ButtonRelease-1>", self.on_release)):
            self.canvas.tag_bind(self.tag, ev, cb)

    def on_click(self, ev):
        logger.debug("Block clicked")
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
        logger.debug("Block released")
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
        logger.info(f"{self.text} block locked")
    
    def unlock(self):
        if self.text != "PRADŽIA":
            self.locked = False
            logger.info(f"{self.text} block unlocked")

    def destroy(self):
        self.canvas.delete(self.tag)

def scale_font(base_size):
    return int(base_size * config.BLOCK_SIZE_COEF)
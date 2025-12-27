from config import *
from utils import load_svg_img
from logger import get_logger, setLoggerLevel
from logging import INFO
from sequence_executor import SequenceExecutor
from ui.error_popup import ErrorPopup
logger = get_logger("Command Line")
setLoggerLevel(logger, INFO)

class CommandLine():
    def __init__(self, app, canvas, canvas_x, y_top, piece_w, piece_h, n_slots, overlap):
        self.canvas, self.piece_w, self.piece_h, self.app, self.n_slots = canvas, piece_w, piece_h, app, n_slots
        self.slot_w  = int(piece_w * (1 - overlap))
        self.slots   = [None] * self.n_slots
        self.sequence_executor = SequenceExecutor()

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
                                          self.x1 + CMD_SIDE_PAD, y1 + CMD_H_PAD, fill=BLACK, 
                                          outline=WHITE, width=3)
        
        self.cmd_img = load_svg_img(app, CMD_BLOCK_PATH, (self.piece_w, self.piece_h))
        

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
            logger.debug("Too far away")
            return False

        # snap!
        tgt_cx = self.x0 + slot*self.slot_w + self.piece_w//2
        dx, dy = tgt_cx - cx, self.y_mid - ((bb[1]+bb[3]) / 2)
        self.canvas.move(block.tag, dx, dy)
        self.slots[slot], block.slot = block, slot
        logger.debug("SNAP!")
        if self.slots[block.slot - 1] is not None:
            self.slots[block.slot - 1].lock()
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        if slot + 1 < self.n_slots:
            self.canvas.create_image(tgt_cx + self.slot_w, self.y_mid, image=self.cmd_img, 
                                                            anchor="center", tags=f"bg_{slot + 1}")
        return True

    def clear(self, event=None):
        logger.info("Clearing...")
        for slot, block in enumerate(self.slots):
            if block is None: 
                logger.info("CLEARED!")
                return
            if block.start: 
                logger.info("start_block skipped")
                continue
            block.destroy()
            self.canvas.delete(f"bg_{slot + 1}")
            self.slots[slot] = None
            block.slot = None
            
        logger.info("CLEARED!")
        return
    
    def submit(self, event):
        logger.info("Block sequence submitted")

        sequence = []

        for block in self.slots:
            if block is None:
                logger.debug("Empty slot detected - stopping")
                break

            action_name = block.text.strip()

            logger.debug(f"Adding action: {action_name}")
            sequence.append(action_name)

        logger.info(f"Final sequence: {sequence}")
        self.sequence_executor.execute(
            sequence=sequence,
            on_hard_error=self.show_hard_error,
            on_soft_error=self.show_soft_error
        )

        return sequence
    
    def show_hard_error(self, title, message):
        ErrorPopup(self.canvas, title, message, level="hard")

    def show_soft_error(self, title, message):
        ErrorPopup(self.canvas, title, message, level="soft")

import os
if "DISPLAY" not in os.environ:   # needed when starting from cron/rc.local
    os.environ["DISPLAY"] = ":0"
import tkinter as tk
from PIL import Image, ImageTk
#import cairosvg, io, re
from pathlib import Path

class PuzzleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.title("Puzzle Command Builder")

        self.sw, self.sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = tk.Canvas(self.root, width=self.sw, height=self.sh, bg = 'black')
        self.canvas.pack(fill="both", expand=True)

        self.root.bind("<Escape>", lambda e: self.root.destroy())
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    PuzzleApp().run()
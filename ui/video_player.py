from PIL import Image, ImageTk
import tkinter as tk
import cv2

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
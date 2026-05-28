import tkinter as tk


class SubmissionOverlay:
    def __init__(self, app):
        self._canvas = app.canvas
        self._rect = self._canvas.create_rectangle(
            0, 0, 9999, 9999,
            fill="#000000", stipple="gray75", outline=""
        )
        self._canvas.update_idletasks()
        self._canvas.grab_set()

    def close(self):
        self._canvas.grab_release()
        self._canvas.delete(self._rect)


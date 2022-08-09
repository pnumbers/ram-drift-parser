import platform

import tkinter as tk
from tkinter import ANCHOR, ttk
from tkinter import filedialog, messagebox

OS_NAME = platform.system()
if OS_NAME == "Darwin":
    from AppKit import NSScreen
elif OS_NAME == "Windows":
    import ctypes

from drift_parser import RamDriftImporter

# Gui Options
APP_WIDTH = 600
APP_HEIGHT = 475
MAPPED_OPTIONS = {"width": 50}


def get_screen_resolution():
    """Returns the screen resolution in [width, heighth]"""
    os_name = platform.system()
    if os_name == "Darwin":
        w = NSScreen.mainScreen().frame().size.width
        h = NSScreen.mainScreen().frame().size.height
    else:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    return [w, h]


class GuiManager(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.set_centered_window_size(APP_WIDTH, APP_HEIGHT)

    def set_centered_window_size(self, width, height):
        self.monitor_screen_size = get_screen_resolution()

        x = int((self.monitor_screen_size[0] - width) / 2)
        y = int((self.monitor_screen_size[1] - height) / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


def main():
    global app
    app = GuiManager()
    app.protocol("WM_DELETE_WINDOW", _quit)
    app.mainloop()


# TODO Breaks when abtracting out main function
def _quit():
    app.quit()
    app.destroy()


# The main function will run the parser.
if __name__ == "__main__":
    main()

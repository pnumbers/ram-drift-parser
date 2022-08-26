from doctest import master
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
        self.title("Ram Drift Tool")
        self.drift_importer = RamDriftImporter()
        self.initialize_window()

    def set_centered_window_size(self, width, height):
        self.monitor_screen_size = get_screen_resolution()

        x = int((self.monitor_screen_size[0] - width) / 2)
        y = int((self.monitor_screen_size[1] - height) / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def initialize_window(self):
        # Root Frame for everything else
        self.menubar = tk.Menu(master=self, background="blue")
        self.config(menu=self.menubar)

        # Menu bar items
        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.settings_menu = tk.Menu(self.menubar, tearoff=False)

        self.file_menu.add_command(label="New")
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.settings_menu.add_command(label="New")
        self.menubar.add_cascade(label="Settings", menu=self.settings_menu)

        # Main Frame for the Main Window
        self.root_frame = tk.LabelFrame(
            master=self, padx=10, pady=10, borderwidth=0, highlightthickness=0
        )
        self.root_frame.grid(row=1, column=0)

        # Import and Refresh Buttons
        self.buttons_frame = tk.LabelFrame(master=self.root_frame, text="Import Data")
        self.buttons_frame.config(padx=10, pady=10)
        self.buttons_frame.pack()

        self.import_button = ttk.Button(
            master=self.buttons_frame,
            text="Import RAM File",
            command=self.import_button_click,
        )
        self.refresh_button = ttk.Button(
            master=self.buttons_frame,
            text="Refresh RAM Data",
            command=self.refresh_button_click,
        )
        self.import_button.pack()
        self.refresh_button.pack()

        # Project Data
        self.project_data_frame = tk.LabelFrame(
            master=self.root_frame, text="Project Data"
        )
        self.project_data_frame.pack()
        self.importance_label = ttk.Label(master=self.project_data_frame, text="Ie = ")
        self.deflect_amp_label = ttk.Label(master=self.project_data_frame, text="Cd = ")

        self.importance_label.pack()
        self.deflect_amp_label.pack()

    def import_button_click(self):
        print("Importing")
        self.drift_importer.set_import_file_path("raw_data_drift_cases.csv")
        self.drift_importer.first_import()

    def refresh_button_click(self):
        print("Refresh")


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

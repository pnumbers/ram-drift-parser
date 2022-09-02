from doctest import master
import platform

import tkinter as tk
from tkinter import ANCHOR, StringVar, ttk
from tkinter import filedialog, messagebox
from turtle import title

OS_NAME = platform.system()
if OS_NAME == "Darwin":
    # TODO: Find new library that will replace AppKit
    # or a way to make AppKit work again
    # from AppKit import NSScreen
    pass
elif OS_NAME == "Windows":
    import ctypes

from drift_parser import RamDriftImporter

# Gui Options
APP_WIDTH = 600
APP_HEIGHT = 475
MAPPED_OPTIONS = {"width": 50}

# TODO: Delete this code if the thkinter version works on windows
def get_screen_resolution():
    """Returns the screen resolution in [width, heighth]"""

    os_name = platform.system()
    if os_name == "Darwin":
        # Fix this so that it correctly takes the screen width and heigth
        # w = NSScreen.mainScreen().frame().size.width
        # h = NSScreen.mainScreen().frame().size.height
        w = 2560 / 2
        h = 1600 / 2
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
        self.initialize_dynamic_variables()
        self.initialize_window()
        self.Ax_ui()
        self.dev_ui()
        # Containers
        self.x_ax = []
        self.y_ax = []

    def set_centered_window_size(self, width, height):
        # TODO: Test on windows. If it works, delete the commented code
        # self.monitor_screen_size = get_screen_resolution()
        # x = int((self.monitor_screen_size[0] - width) / 2)
        # y = int((self.monitor_screen_size[1] - height) / 2)
        x = int((self.winfo_screenwidth() - width) / 2)
        y = int((self.winfo_screenheight() - height) / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def initialize_dynamic_variables(self):
        """Initializes the dynamic variables for GUI"""
        self.input_file_var = tk.StringVar(master=self, value="RAM Drift File:")

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
        self.allowable_drift_label = ttk.Label(
            master=self.project_data_frame, text="Δa= "
        )

        self.importance_label.pack()
        self.deflect_amp_label.pack()
        self.allowable_drift_label.pack()

        self.input_file_label = ttk.Label(
            master=self.root_frame, textvariable=self.input_file_var, wraplength=500
        )
        self.input_file_label.pack()

    def import_button_click(self):
        """Imports a RAM drift file from a user selected file."""
        ram_filepath = self.get_input_filepath()
        if self.drift_importer.set_import_file_path(ram_filepath):
            self.drift_importer.first_import()
            self.input_file_var.set(f"RAM Drift File: \n{ram_filepath}")

    def refresh_button_click(self):
        print("Refresh")

    def file_not_found_message(self) -> None:
        """Generates a 'File not found.' dialog message"""
        # root = tk.Tk()
        # root.withdraw()
        warning_message = "No file chosen. Import canceled."
        messagebox.showinfo(title=None, message=warning_message)

    def get_input_filepath(self) -> str:
        """Generates a filedialog for getting the input file."""

        filepath = filedialog.askopenfilename(title="Load RAM Drift CSV File")

        # Taken from dirootsimporter
        # if self.input_filepath == None:
        #     if not self.get_input_filepath():
        #         self.file_not_found_message()

        # if self.input_filepath == "":
        #     raise FileNotFoundError
        return filepath

    # Dev_UI Elements
    def dev_ui(self):
        self.dev_frame = tk.LabelFrame(master=self, text="Dev Frame")
        self.dev_frame.grid(row=1, column=1)

        self.print_stories_btn = ttk.Button(
            master=self.dev_frame,
            text="Print Stories",
            command=self.print_stories_btn_click,
        )
        self.print_stories_btn.pack()

        self.set_stories_btn = ttk.Button(
            master=self.dev_frame,
            text="Set Story Heights",
            command=self.create_story_input_window,
        )
        self.set_stories_btn.pack()

        self.print_Ax_btn = ttk.Button(
            master=self.dev_frame,
            text="Print Ax Values",
            command=self.set_ax_values,
        )
        self.print_Ax_btn.pack()

    def print_stories_btn_click(self):
        self.drift_importer.print_data()

    def create_story_input_window(self):
        self.story_window = tk.Toplevel(master=self, height=450, width=600)

    # Set Ax values on main UI
    def Ax_ui(self):
        """Initialize the Ax UI elements"""

        self.x_ax = []
        self.y_ax = []

        self.ax_frame = tk.LabelFrame(master=self, text="Ax Values")
        self.ax_frame.grid(row=1, column=2)

        self.x_axis_frame = tk.LabelFrame(master=self.ax_frame, text="X-axis")
        self.x_axis_frame.grid(row=0, column=0)

        self.y_axis_frame = tk.LabelFrame(master=self.ax_frame, text="Y-axis")
        self.y_axis_frame.grid(row=0, column=1)

        # Set starting Ax elments until data is loaded
        # self.

    def set_ax_values(self):
        """Update the Ax UI elements

        This needs to be run after the first import and upon each new
        import to ensure the data is current.
        """
        # Destroy elements of ax_ui and clear the array so that
        # the values can be reset
        # TODO: Change these elements to be var elemnts so that destroying
        #       them isnt required. This would however need to account for possible
        #       change in number of floors or floor name changes
        self.clear_ax_ui()

        # Creates new UI Elements
        data = self.drift_importer.torsion_data
        for story in self.drift_importer.stories:
            ax = data["X-Axis"][story]["Ax"]
            # ttk.Label(self.x_axis_frame, text=f"{story}: {ax}").pack()
            self.x_ax.append(ttk.Label(self.x_axis_frame, text=f"{story}: {ax}"))

        for el in self.x_ax:
            el.pack()

        for story in self.drift_importer.stories:
            ax = data["Y-Axis"][story]["Ax"]
            # ttk.Label(self.y_axis_frame, text=f"{story}: {ax}").pack()
            self.y_ax.append(ttk.Label(self.y_axis_frame, text=f"{story}: {ax}"))

        for el in self.y_ax:
            el.pack()

        # self.drift_importer.print_Ax_values()
        # print(self.drift_importer.torsion_data)

    def clear_ax_ui(self):
        for el in self.x_ax:
            el.destroy()
        self.x_ax.clear()

        for el in self.y_ax:
            el.destroy()
        self.y_ax.clear()


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

from doctest import master
import platform

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

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
APP_WIDTH = 1200
APP_HEIGHT = 700
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
        self.drift_ui()
        self.stories_ui()
        # Containers
        # self.x_ax = []
        # self.y_ax = []

    def set_centered_window_size(self, width, height) -> None:
        """Set the root window in the center of the screen."""

        # TODO: Test on windows. If it works, delete the commented code
        # self.monitor_screen_size = get_screen_resolution()
        # x = int((self.monitor_screen_size[0] - width) / 2)
        # y = int((self.monitor_screen_size[1] - height) / 2)
        x = int((self.winfo_screenwidth() - width) / 2)
        y = int((self.winfo_screenheight() - height) / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def initialize_dynamic_variables(self) -> None:
        """Initializes the dynamic variables for GUI"""

        self.input_file_var = tk.StringVar(master=self, value="RAM Drift File:")

    #
    # Main Window Code **************************************************
    # TODO: Break this up into smaller chunks

    def initialize_window(self) -> None:
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
        self.root_frame.grid(row=0, column=0)

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

    def import_button_click(self) -> None:
        """Imports a RAM drift file from a user selected file."""

        ram_filepath = self.get_input_filepath()
        if self.drift_importer.set_import_file_path(ram_filepath):
            self.drift_importer.first_import()
            self.input_file_var.set(f"RAM Drift File: \n{ram_filepath}")

        self.set_story_rows()

    def refresh_button_click(self) -> None:
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

    #
    # Dev_UI Elements Code **********************************************
    def dev_ui(self):
        """Initializes a frame for development ui elements.

        This frame is used to place elements that are for development purposes or to place
        elements that do not have a set place in the production UI yet."""

        self.dev_frame = tk.LabelFrame(master=self, text="Dev Frame")
        self.dev_frame.grid(row=0, column=1)

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
        self.set_story_rows()

    def create_story_input_window(self):
        self.story_window = tk.Toplevel(master=self, height=450, width=600)

    #
    # Drift UI Code *****************************************************

    def drift_ui(self) -> None:
        """Initialize the drift UI elements."""

        self.drift_frame = tk.LabelFrame(master=self, text="Drifts")
        self.drift_frame.grid(row=1, column=1)

        self.blank = tk.Label(master=self.drift_frame, text="Drift stuff")
        self.blank.pack()

    #
    # Stories UI Code ***************************************************

    def stories_ui(self) -> None:
        """Initialize the stories UI elements."""

        self.story_elements = []
        self.story_height_elements = []

        self.stories_frame = tk.LabelFrame(
            master=self, text="Story Heights", padx=10, pady=10
        )
        self.stories_frame.grid(row=2, column=0)

        self.story_list_frame = tk.Frame(master=self.stories_frame)
        self.story_list_frame.grid(row=0, column=0, columnspan=2)

        self.save_heights_btn = ttk.Button(
            master=self.stories_frame,
            text="Save Heights",
            command=self.save_heights_btn_click,
        )
        self.save_heights_btn.grid(row=1, column=1)

        self.change_heights_btn = ttk.Button(
            master=self.stories_frame,
            text="Change Heights",
            command=self.change_heights_btn_click,
            state="disabled",
        )
        self.change_heights_btn.grid(row=1, column=0)

        # self.story_header = tk.Entry(master=self.story_list_frame, text="Story:")
        # self.story_header.insert(0, "Story: ")
        # self.story_header.config(state="disabled")
        self.story_header = tk.Label(master=self.story_list_frame, text="Story:")
        self.story_header.grid(row=0, column=0)

        self.height_header = tk.Label(master=self.story_list_frame, text="Height (ft):")
        self.height_header.grid(row=0, column=1)

        self.set_story_rows()

    def set_story_rows(self) -> None:
        for i, story in enumerate(self.drift_importer.stories, 1):
            el = tk.Label(master=self.story_list_frame, text=f"{story}: ")
            el.grid(row=i, column=0)
            self.story_elements.append(el)

            entry = ttk.Entry(master=self.story_list_frame, width=12)
            entry.grid(row=i, column=1)
            self.story_height_elements.append(entry)

        self.total_height_label = tk.Label(master=self.story_list_frame, text="Total: ")
        total_row = 2 + len(self.story_elements)
        self.total_height_label.grid(row=total_row, column=0)

        self.total_height_val_label = tk.Label(
            master=self.story_list_frame, text="0 ft"
        )
        self.total_height_val_label.grid(row=total_row, column=1)

    def change_heights_btn_click(self):
        """Activates the story heights save button and the story heights entry boxes."""

        self.change_heights_btn.config(state="disabled")
        self.save_heights_btn.config(state="active")

        for el in self.story_height_elements:
            el.config(state="active")

    def save_heights_btn_click(self):
        self.change_heights_btn.config(state="active")
        self.save_heights_btn.config(state="disabled")

        story_heights_dict = {}

        for i, el in enumerate(self.story_height_elements):
            height = el.get()
            el.config(state="disabled")
            story = self.story_elements[i]["text"]
            story_heights_dict[story] = float(height)

        self.drift_importer.set_story_heights(story_heights_dict)
        total_height = self.drift_importer.total_height
        self.total_height_val_label.config(text=f"{total_height} ft")

    #
    # Ax UI Code ********************************************************

    # Set Ax values on main UI
    def Ax_ui(self) -> None:
        """Initialize the Ax UI elements."""

        self.x_ax = []
        self.y_ax = []

        self.ax_frame = tk.LabelFrame(master=self, text="Ax Values")
        self.ax_frame.grid(row=0, column=2, pady=20)

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

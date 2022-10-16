from cgi import test
from doctest import master
import platform
from textwrap import fill

import tkinter as tk
from tkinter import RIGHT, Y, ttk
from tkinter import *
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

# DEV
DEV_MODE = False
if DEV_MODE:
    INPUT_FILE_DEV = "raw_data_drift_cases.csv"

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
        # Containers
        # self.x_ax = []
        # self.y_ax = []

    def set_centered_window_size(self, width, height) -> None:
        """Set the root window in the center of the screen."""
        # width = 0
        # height = 0
        # screen_width = self.winfo_screenwidth()
        # screen_height = self.winfo_screenheight()
        # TODO: Test on windows. If it works, delete the commented code
        # self.monitor_screen_size = get_screen_resolution()
        # x = int((self.monitor_screen_size[0] - width) / 2)
        # y = int((self.monitor_screen_size[1] - height) / 2)
        x = int((self.winfo_screenwidth() - width) / 2)
        y = int((self.winfo_screenheight() - height) / 2)

        # x = 0
        # y = 0
        self.geometry(f"{width}x{height}+{x}+{y}")
        # self.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

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

        # Initialize root window components
        self.import_ui()
        self.Ax_ui()
        self.drift_ui()
        self.stories_ui()
        self.project_data_ui()
        # Development UI self places into the root GUI window
        if DEV_MODE:
            self.dev_ui()

        # self.import_ui_frame.grid(row=0, column=0)
        self.import_ui_frame.grid(row=0, column=2)
        self.ax_ui_frame.grid(row=1, column=0)
        self.drift_ui_frame.grid(row=1, column=0, columnspan=2)
        self.stories_ui_frame.grid(row=1, column=2)
        self.project_data_ui_frame.grid(row=0, column=0)

        # TODO: Find a place to put this file label
        #           -> Place at the bottom of the screen
        # TODO: Truncate / make this file path shorter when displayed
        self.input_file_label = ttk.Label(
            master=self.root_frame, textvariable=self.input_file_var, wraplength=500
        )
        self.input_file_label.grid(row=3, column=0)

    #
    # Project_data_UI Elements code *******************************************
    def project_data_ui(self):
        """Initialize project data frame."""

        self.project_data_ui_frame = tk.LabelFrame(
            master=self.root_frame, text="Seismic Project Data", padx=10, pady=10
        )
        # self.project_data_ui_frame.pack()
        self.importance_label = ttk.Label(
            master=self.project_data_ui_frame, text="Importance Factor: Ie = "
        )
        self.deflect_amp_label = ttk.Label(
            master=self.project_data_ui_frame, text="Deflection Amplification: Cd = "
        )
        self.allowable_drift_label = ttk.Label(
            master=self.project_data_ui_frame, text="Allowable Deflection: Δa = "
        )

        self.importance_entry = ttk.Entry(master=self.project_data_ui_frame, width=10)
        self.deflect_amp_entry = ttk.Entry(master=self.project_data_ui_frame, width=10)
        self.allowable_drift_entry = ttk.Entry(
            master=self.project_data_ui_frame, width=10
        )

        self.importance_label.grid(row=0, column=0, sticky="E")
        self.deflect_amp_label.grid(row=1, column=0, sticky="E")
        self.allowable_drift_label.grid(row=2, column=0, sticky="E")

        self.importance_entry.grid(row=0, column=1, pady=2)
        self.deflect_amp_entry.grid(row=1, column=1, pady=2)
        self.allowable_drift_entry.grid(row=2, column=1, pady=2)

        self.project_data_save_btn = ttk.Button(
            master=self.project_data_ui_frame,
            text="Save",
            command=self.project_data_save_click,
        )
        self.project_data_save_btn.grid(row=3, column=1, pady=3)

    def project_data_save_click(self) -> None:
        """Push the project data entries to the drift parser."""

        importance_factor = float(self.importance_entry.get())
        deflect_amp = float(self.deflect_amp_entry.get())
        allowable_drift = float(self.allowable_drift_entry.get())
        self.drift_importer.importance_factor = importance_factor
        self.drift_importer.drift_amp_factor = deflect_amp
        self.drift_importer.allowable_drift_limit = allowable_drift

        self.importance_entry.config(state="disabled")
        self.deflect_amp_entry.config(state="disabled")
        self.allowable_drift_entry.config(state="disabled")

        self.project_data_save_btn.config(
            text="Change", command=self.project_data_change_click
        )

    def project_data_change_click(self) -> None:
        """Active the project data entries boxes."""

        self.importance_entry.config(state="active")
        self.deflect_amp_entry.config(state="active")
        self.allowable_drift_entry.config(state="active")

        self.project_data_save_btn.config(
            text="Save", command=self.project_data_save_click
        )

    #
    # Import_UI Elements Code **********************************************
    def import_ui(self) -> None:
        """Initialize import buttons frame."""
        self.import_ui_frame = tk.Frame(master=self.root_frame)
        self.buttons_frame = tk.LabelFrame(
            master=self.import_ui_frame, text="Import Data"
        )
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

    def import_button_click(self) -> None:
        """Imports a RAM drift file from a user selected file."""

        ram_filepath = self.get_input_filepath()
        self.import_process(ram_filepath)

    def import_process(self, import_file):
        """Run the processes associated with importing a RAM drift file"""

        ram_filepath = import_file
        if self.drift_importer.set_import_file_path(ram_filepath):
            self.drift_importer.first_import()
            self.input_file_var.set(f"RAM Drift File: \n{ram_filepath}")

        self.set_story_rows()

        # Display Ax values on import
        # TODO: Wipe Ax components and display "No drift data" or something
        #       if non-drift case file is loaded
        if self.drift_importer.torsion_data == None:
            print("No torsion data")
        else:
            self.set_ax_values()

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
        # self.drift_importer.print_data()
        # self.set_story_rows()
        print(self.drift_importer.get_overall_heights())
        self.drift_importer.set_drift_limits()
        self.drift_importer.drift_ultilization()

    def create_story_input_window(self):
        self.story_window = tk.Toplevel(master=self, height=450, width=600)

    #
    # Drift UI Code *****************************************************

    def drift_ui(self) -> None:
        """Initialize the drift UI elements."""

        self.drift_ui_frame = tk.LabelFrame(master=self.root_frame, text="Drifts")
        # self.drift_ui_frame.config(width=800, height=800, padx=10, pady=10)
        # self.drift_ui_frame.pack_propagate(False)
        # self.drift_ui_frame.config(width=600, height=500)

        # self.drift_ui_frame.config(padx=10, pady=10)

        # self.drift_ui_frame.grid(row=2, column=1)

        # self.blank = tk.Label(master=self.drift_ui_frame, text="Drift stuff")
        # self.blank.pack()

        # Add drift loop
        self.drift_elements = []
        self.drift_btn = ttk.Button(
            master=self.drift_ui_frame, text="Update Drift", command=self.update_drift
        )
        self.drift_btn.pack()

        self.drift_ui_frame_inner = tk.LabelFrame(
            master=self.drift_ui_frame, text="Drift Data"
        )
        self.drift_ui_frame_inner.pack()
        self.drift_ui_frame_inner_top = tk.Frame(master=self.drift_ui_frame_inner)
        self.drift_ui_frame_inner_top.pack()
        self.drift_ui_frame_inner_bottom = tk.Frame(master=self.drift_ui_frame_inner)
        self.drift_ui_frame_inner_bottom.pack(fill=X)
        # self.drift_ui_frame_inner.config(width=300, height=300)
        # self.drift_ui_frame_inner.pack_propagate(False)

        self.drift_canvas = tk.Canvas(master=self.drift_ui_frame_inner_top)
        self.drift_canvas.pack(side=LEFT)
        self.drift_canvas.config(height=400, width=700)

        # self.drift_ui_frame_inner.bind("<Configure>", self.reset_scrollregion)
        # self.drift_canvas.bind("<Configure>", print("HI"))

        self.drift_scroll_bar_y = tk.Scrollbar(
            master=self.drift_ui_frame_inner_top,
            orient="vertical",
        )
        self.drift_scroll_bar_y.pack(side=RIGHT, fill=Y)

        self.drift_scroll_bar_x = tk.Scrollbar(
            master=self.drift_ui_frame_inner_bottom,
            orient="horizontal",
        )
        self.drift_scroll_bar_x.pack(side=BOTTOM, fill=X)

        self.drift_values_frame = tk.Frame(
            master=self.drift_canvas,
        )
        self.drift_canvas.create_window(
            (0, 0), window=self.drift_values_frame, anchor="nw"
        )

        self.set_drift_values_titles()

        self.drift_canvas.config(yscrollcommand=self.drift_scroll_bar_y.set)
        self.drift_canvas.config(xscrollcommand=self.drift_scroll_bar_x.set)
        self.drift_scroll_bar_y.config(command=self.drift_canvas.yview)
        self.drift_scroll_bar_x.config(command=self.drift_canvas.xview)

        self.drift_values_frame.bind("<Configure>", self.reset_scrollregion)

    def reset_scrollregion(self, event):
        self.drift_canvas.configure(scrollregion=self.drift_canvas.bbox("all"))

    def set_drift_values_titles(self):
        self.drift_title = tk.Label(
            master=self.drift_values_frame, text="Control Points"
        )
        self.drift_title.grid(row=0, column=0)

        self.drift_title = tk.Label(master=self.drift_values_frame, text="Story")
        self.drift_title.grid(row=0, column=1)

        self.drift_title = tk.Label(master=self.drift_values_frame, text="Load Case")
        self.drift_title.grid(row=0, column=2)

        self.drift_title = tk.Label(master=self.drift_values_frame, text="Disp.")
        self.drift_title.grid(row=0, column=3)

        self.drift_title = tk.Label(master=self.drift_values_frame, text="Max Disp.")
        self.drift_title.grid(row=0, column=4)

        self.drift_title = tk.Label(master=self.drift_values_frame, text="Story Drift")
        self.drift_title.grid(row=0, column=5)

        self.drift_title = tk.Label(master=self.drift_values_frame, text="Max Drift")
        self.drift_title.grid(row=0, column=6)

        self.drift_title = tk.Label(master=self.drift_values_frame, text="Drift Ratio")
        self.drift_title.grid(row=0, column=7)

    def update_drift(self):
        for element in self.drift_elements:
            element.destroy()

        n_row = 1
        drift_data = self.drift_importer.drift_data
        for i, cp in enumerate(drift_data):
            stories = self.drift_importer.drift_data[cp]["drifts"]

            label = tk.Label(master=self.drift_values_frame, text=f"{cp}")
            label.grid(row=n_row, column=0)
            self.drift_elements.append(label)

            for story, load_cases in stories.items():
                story_label = tk.Label(master=self.drift_values_frame, text=f"{story}")
                story_label.grid(row=n_row, column=1)
                self.drift_elements.append(story_label)

                for load_case, load_case_data in load_cases.items():
                    case_label = tk.Label(
                        master=self.drift_values_frame, text=f"{load_case}"
                    )
                    case_label.grid(row=n_row, column=2)
                    self.drift_elements.append(case_label)

                    # disp_label = tk.Label(master=self.drift_values_frame, text=f"{load_case_data['displacement']}")
                    # disp_label.grid(row=n_row, column=3)
                    # self.drift_elements.append(disp_label)
                    column_n = 3
                    for data in load_case_data:
                        data_label = tk.Label(
                            master=self.drift_values_frame,
                            text=f"{load_case_data[data]}",
                        )
                        data_label.grid(row=n_row, column=column_n)
                        self.drift_elements.append(data_label)
                        column_n += 1

                    n_row += 1
        # print(self.drift_canvas.bbox("all"))
        # self.drift_canvas.config(scrollregion=self.drift_canvas.bbox("all"))

    #
    # Stories UI Code ***************************************************

    def stories_ui(self) -> None:
        """Initialize the stories UI elements."""

        self.story_elements = []
        self.story_height_elements = []

        self.stories_ui_frame = tk.LabelFrame(
            master=self.root_frame, text="Story Heights", padx=10, pady=10
        )
        # self.stories_ui_frame.grid(row=2, column=0)

        self.story_list_frame = tk.Frame(master=self.stories_ui_frame)
        self.story_list_frame.grid(row=0, column=0, columnspan=2)

        # self.total_height_frame = tk.Frame(master=self.stories_ui_frame)
        # self.total_height_frame.grid(row=1, column=0, columnspan=2)

        # self.total_height_label = tk.Label(
        #     master=self.total_height_frame, text="Total: "
        # )
        # self.total_height_label.grid(row=0, column=0)

        # self.total_height_val_label = tk.Label(
        #     master=self.total_height_frame, text="0 ft"
        # )
        # self.total_height_val_label.grid(row=0, column=1)

        self.save_heights_btn = ttk.Button(
            master=self.stories_ui_frame,
            text="Save Heights",
            command=self.save_heights_btn_click,
        )
        self.save_heights_btn.grid(row=2, column=1)

        self.change_heights_btn = ttk.Button(
            master=self.stories_ui_frame,
            text="Change Heights",
            command=self.change_heights_btn_click,
            state="disabled",
        )
        self.change_heights_btn.grid(row=2, column=0)

        # self.story_header = tk.Entry(master=self.story_list_frame, text="Story:")
        # self.story_header.insert(0, "Story: ")
        # self.story_header.config(state="disabled")
        self.story_header = tk.Label(master=self.story_list_frame, text="Story:")
        self.story_header.grid(row=0, column=0)

        self.height_header = tk.Label(master=self.story_list_frame, text="Height (ft):")
        self.height_header.grid(row=0, column=1)

        self.set_story_rows()

    def set_story_rows(self) -> None:
        """Create labels and entry boxes for each story."""

        # Clears the story_list_frame elements
        for el in self.story_elements:
            el.destroy()

        for el in self.story_height_elements:
            el.destroy()

        # TODO: Loop through and destroy elements before they are made
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

        self.story_elements.append(self.total_height_label)
        self.story_height_elements.append(self.total_height_val_label)

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
            story = self.story_elements[i]["text"][:-2]
            story_heights_dict[story] = float(height)

        # self.drift_importer.set_story_heights(story_heights_dict)
        # total_height = self.drift_importer.total_height
        # self.total_height_val_label.config(text=f"{total_height} ft")

    #
    # Ax UI Code ********************************************************

    # Set Ax values on main UI
    def Ax_ui(self) -> None:
        """Initialize the Ax UI elements."""

        self.x_ax = []
        self.y_ax = []

        self.ax_ui_frame = tk.LabelFrame(master=self.root_frame, text="Ax Values")
        self.ax_ui_frame.config(pady=20)
        # self.ax_ui_frame.grid(row=0, column=2, pady=20)

        self.x_axis_frame = tk.LabelFrame(master=self.ax_ui_frame, text="X-axis")
        self.x_axis_frame.grid(row=0, column=0)

        self.y_axis_frame = tk.LabelFrame(master=self.ax_ui_frame, text="Y-axis")
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


def dev_run(app):
    """Run the development mode functions"""

    app.import_process(INPUT_FILE_DEV)


def main():
    global app
    app = GuiManager()

    # Runs the development function
    if DEV_MODE:
        dev_run(app)

    app.protocol("WM_DELETE_WINDOW", _quit)
    app.mainloop()


# TODO Breaks when abtracting out main function
def _quit():
    app.quit()
    app.destroy()


# The main function will run the parser.
if __name__ == "__main__":
    main()

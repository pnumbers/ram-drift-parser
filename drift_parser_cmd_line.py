from xmlrpc.client import Boolean
from drift_parser import RamDriftImporter
import os


class DriftCommandLine:
    def __init__(self) -> None:
        self.drift_importer = RamDriftImporter()
        self.main_loop_on = True
        self.main_loop()

    def main_loop(self) -> None:
        os.system("CLS||clear")
        print("************     Welcome to the RAM Drift Importer!     ************")
        while self.main_loop_on:

            self.report_input_info()
            self.print_main_menu()
            selection = input("Selection: ").strip().lower()

            if selection == "q" or selection == "quit":
                self.main_loop_on = False

            match selection:
                case "1":
                    filepath = input("Provide filepath to import: ")
                    if not self.drift_importer.set_import_file_path(filepath):
                        print("\nFilepath does not exist.")
                        continue
                    else:
                        # self.drift_importer.import_drift_data()
                        # self.drift_importer.parse_data()
                        self.drift_importer.first_import()

                case "2":
                    if self.drift_importer.import_file_path:
                        self.drift_importer.reimport()
                        print("Import successful")
                    else:
                        print("No import file found. Press 1 to provide an import file")

                case "3":
                    if self.drift_importer.data == None:
                        msg = """
                        No story data available. Import a ram drift csv file
                        prior to setting story heights."""
                        print(msg)
                    else:
                        self.set_story_heights()

                case "4":
                    self.set_project_values()

                case "5":
                    self.report_Ax()
        return None

    def import_file(self) -> bool:
        filepath = input("Provide filepath to import: ")
        if not self.drift_importer.set_import_file_path(filepath):
            print("\nFilepath does not exist.")
            return False
        print("Import successful.")
        self.drift_importer.parse_data()
        self.drift_importer.print_data()
        return True

    def report_input_info(self) -> None:
        info = f"""
        ****** Input Info *********
        Input file: {self.drift_importer.import_file_path}
        """
        print('\n****** Input Info *********')
        print(f'Input file: {self.drift_importer.import_file_path}')
        return None

    def report_Ax(self):
        self.drift_importer.print_Ax_values()
        input('\nPress any key to continue...')
    
    def print_main_menu(self) -> None:
        msg = """
            ******    Menu    ******
            1) Set RAM Data File & Import
            2) Re-import Data
            3) Set Story Heights
            4) Set Project Values
            5) Report "Ax" Values
            6) Report Drift Percentages    (Coming Soon)
        
            q) Quit (quit or q)
            """
        print(msg)
        return None

    def set_story_heights(self) -> None:
        """Requests user input to set the story heights"""
        # TODO: Split up this function into a setter function and put
        #       the cmdline functionality in the cmd_line class
        height_dict = {}
        for story in self.drift_importer.stories:
            height_dict[story] = float(input(f"{story} (ft): "))
        self.drift_importer.set_story_heights(height_dict)
        self.drift_importer.set_total_height()

    def set_project_values(self):
        importance_factor = input("Set Project Importance Factor: ")
        

def main():
    root = DriftCommandLine()


if __name__ == "__main__":
    main()

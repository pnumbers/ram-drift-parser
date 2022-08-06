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

            # if selection == "1":
            #     filepath = input("Provide filepath to import: ")
            #     if not self.drift_importer.set_import_file_path(filepath):
            #         print("\nFilepath does not exist.")
            #         continue

            match selection:
                case "1":
                    filepath = input("Provide filepath to import: ")
                    if not self.drift_importer.set_import_file_path(filepath):
                        print("\nFilepath does not exist.")
                        continue
                    else:
                        self.drift_importer.import_drift_data()
                        self.drift_importer.parse_data()

                case "2":
                    if self.drift_importer.data == None:
                        msg = """
                        No story data available. Import a ram drift csv file
                        prior to setting story heights."""
                        print(msg)
                    else:
                        self.drift_importer.set_story_heights()
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
        # print(info)
        return None

    
    def print_main_menu(self) -> None:
        msg = """
            ******    Menu    ******
            1) Import File
            2) Set Story Heights
            3) Report "Ax" Values          (Coming Soon)
            4) Report Drift Percentages    (Coming Soon)
        
            q) Quit (quit or q)
            """
        print(msg)
        return None



def main():
    root = DriftCommandLine()


if __name__ == "__main__":
    main()

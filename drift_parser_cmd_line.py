from drift_parser import RamDriftImporter
import os


class DriftCommandLine:
    def __init__(self) -> None:
        self.drift_importer = RamDriftImporter()
        self.main_loop_on = True
        self.main_loop()

    def main_loop(self):
        os.system("CLS")
        print("************     Welcome to the RAM Drift Importer!     ************")
        while self.main_loop_on:

            self.report_input_info()

            msg = """
            ******    Menu    ******
            1) Import File
            2) Set Story Heights
            3) Report "Ax" Values          (Coming Soon)
            4) Report Drift Percentages    (Coming Soon)
        
            q) Quit (quit or q)
            """
            print(msg)
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
                        self.drift_importer.parse_data()

                case "2":
                    self.drift_importer.set_story_heights()

    def import_file(self):
        filepath = input("Provide filepath to import: ")
        if not self.drift_importer.set_import_file_path(filepath):
            print("\nFilepath does not exist.")
            return False
        print("Import successful.")
        self.drift_importer.parse_data()
        self.drift_importer.print_data()
        return True

    def report_input_info(self):
        info = f"""
        ****** Input Info *********
        Input file: 
        """


def main():
    root = DriftCommandLine()


if __name__ == "__main__":
    main()

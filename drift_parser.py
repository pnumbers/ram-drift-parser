import csv
from dataclasses import dataclass
import re
import os

FILE = "raw_data.csv"
FILE_PATH = FILE

# TODO Add in arg parsing for commandline runs
# TODO Create a way to parse drfit outputs to give deflections
# TODO Add in commandline output of deflections and torsion irregularity
# TODO Add in support to parse the data for torsional irregularity without
# the use of RAM's torsional data based on the drift only cases
class RamDriftImporter:
    """A class that imports and parses drift output from RAM Structural
    System's Frame module. This class requires control points to have
    been set in RAM Frame."""

    def __init__(self, import_file_path=None) -> None:
        self.import_file_path = import_file_path
        self.data = None
        # Indexes for the section dividers of the data array
        self.results_title_index = None
        self.load_cases_title_index = None
        self.torsional_title_index = None
        # Data containers for the parsed data
        self.load_cases = {}
        self.drift_data = {}
        self.torsion_data = {}
        # Automatically run the parser if an input file is given
        if self.import_file_path and os.path.exists(self.import_file_path):
            self.import_drift_data()
            self.parse_data()
            return (self.load_cases, self.drift_data, self.torsion_data)

    def import_drift_data(self) -> None:
        """Imports the raw data csv file from RAM and stores the data
        in an arrary 'self.data'"""
        with open(self.import_file_path, "r") as file:
            reader = csv.reader(file)
            self.data = [row for row in reader]

    def get_section_indexes(self) -> None:
        """Gets the indexes of the 'LOAD CASE DEFINITIONS', 'RESULTS', and
        TORSIONAL IRREGULARITY DATA' sections headers."""
        for i, row in enumerate(self.data):
            if row[0] == "LOAD CASE DEFINITIONS:":
                self.load_cases_title_index = i

            if row[0] == "RESULTS:":
                self.results_title_index = i

            if row[0] == "TORSIONAL IRREGULARITY DATA:":
                self.torsional_title_index = i

    def get_load_cases(self) -> None:
        for i in range(self.load_cases_title_index + 1, self.results_title_index):
            load_case = self.data[i]
            if "DRIFT" in load_case[1]:
                load_case_code = load_case[0].strip()
                load_case_name = load_case[1].strip()
                load_case_equation = load_case[2].strip()
                self.load_cases[load_case_code] = [
                    load_case_name,
                    load_case_equation,
                ]

    def parse_drift_data(self):
        self.drift_data = {}

        control_point_number = 0
        control_point_data = None
        control_point_name = None
        location = None
        story = None

        # Loop through the drift data block. This includes header
        # information for each control point
        for i in range(self.results_title_index + 1, self.torsional_title_index):
            row = self.data[i]
            # print(row)

            # If this triggers then a new control point has been begun in the
            # data block
            if "Location" in row[0]:
                # Adds the previous control points to the drift_data dict
                if control_point_data:
                    self.drift_data[control_point_name] = control_point_data
                control_point_number += 1
                x = re.search("\(-*\d+.\d*", row[0]).group(0)[1:]
                y = row[1].strip()[:-1]
                location = [x, y]
                control_point_name = "CP" + str(control_point_number)
                control_point_data = {"location": location, "drifts": {}}
                continue

            # Checks to see if this is a row that starts a new story. If so
            # it saves the story name
            if row[0] != "" and row[0].strip() != "Story":
                story = row[0].strip()
                control_point_data["drifts"][story] = {}

            # Checks to see if the row is a drift load case. If so it adds the
            # data to the control point
            if row[1].strip() in self.load_cases:
                load_case = row[1].strip()
                displacement = [float(x) for x in row[2:4]]
                story_drift = [float(x) for x in row[4:6]]
                drift_ratio = [float(x) for x in row[6:]]

                data = {}
                data["displacement"] = displacement
                data["story_drift"] = story_drift
                data["drift_ratio"] = drift_ratio

                control_point_data["drifts"][story][load_case] = data

        # Adds the final control point to the drift data
        self.drift_data[control_point_name] = control_point_data

    def parse_torsional_data(self):
        """Parses the 'Torsional Irregularity Data from the input file"""
        axis = None
        for i in range(self.torsional_title_index + 1, len(self.data)):
            row = self.data[i]
            if "-Axis" in row[0]:
                if axis:
                    self.torsion_data[axis] = axis_dict
                axis = row[0]
                axis_dict = {}
                skip = 2
                continue

            if skip:
                skip -= 1
                continue

            story = row[0]
            load_case = row[1]
            # Check is the load case is not a drift case. If it is not a
            #  drift case then the data is not valid
            if load_case not in self.load_cases:
                self.torsion_data = None
                break

            max_drift = float(row[2])
            x = re.search("\(-?\d+.\d*", row[3]).group(0)[1:]
            y = re.search("\s-?\d+.\d*", row[3]).group(0)[1:]
            max_drift_coord = (float(x), float(y))

            min_drift = float(row[4])
            x = re.search("\(-?\d+.\d*", row[5]).group(0)[1:]
            y = re.search("\s-?\d+.\d*", row[5]).group(0)[1:]
            min_drift_coord = (float(x), float(y))

            max_div_min = float(row[6])
            max_div_avg = float(row[7])
            Ax = round(min(max(((max_div_avg / 1.2) ** 2), 1), 3), 4)
            percent_eccentricity = round(Ax * 0.05 * 100, 4)

            story_dict = {}
            story_dict["Load Case"] = load_case
            story_dict["Max Drift"] = max_drift
            story_dict["Max Drift Coord"] = max_drift_coord
            story_dict["Min Drift"] = min_drift
            story_dict["Min Drift Coord"] = min_drift_coord
            story_dict["Max/Min"] = max_div_min
            story_dict["Max/Avg"] = max_div_avg
            story_dict["Ax"] = Ax
            story_dict["Eccentricity"] = percent_eccentricity

            axis_dict[story] = story_dict

        # Add final axis dictionary to class torsion data
        if self.torsion_data:
            self.torsion_data[axis] = axis_dict

    def parse_data(self):
        self.get_section_indexes()
        self.get_load_cases()
        self.parse_drift_data()
        self.parse_torsional_data()

    # This function isn't currently all that useful. It prints too
    # data and the data is too messy to read. Consider a better way to
    # handle this. Also consider if this is necessary.
    def print_data(self):
        print(self.load_cases)
        print(self.drift_data)
        print(self.torsion_data)


def main():
    drift_importer = RamDriftImporter(FILE_PATH)
    # drift_importer.import_drift_data()
    # drift_importer.parse_data()
    # drift_importer.print_data()


if __name__ == "__main__":
    main()


# @dataclass
# class DriftRatio:
#     """Class for storying driftratios"""


"""
Data Schema for control points

{
    cp#:
        location: [x,y],
        drifts: {
            story: {
                load_case: {
                    displacement: [],
                    story_drift: [],
                    drift_ratio: []
                    }
                }
            }
        }
}

What if we used dataclasses for this data?
What if we used a built-up hash key for the displacement data?
ie CP#_Story_LoadCase = {}
ex: CP2_Roof_E6 = {}

cp#.drifts.story.displacement.x
"""

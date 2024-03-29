from typing import List, Set, Dict, Tuple, Optional
from dataclasses import dataclass

import csv
import re
import os

FILE = "raw_data_drift_cases.csv"
# FILE = "raw_data.csv"
FILE_PATH = FILE

# TODO: Add in arg parsing for commandline runs
# TODO: Create a way to parse drfit outputs to give deflections
# TODO: Add in commandline output of deflections and torsion irregularity
# TODO: Add in support to parse the data for torsional irregularity without
# the use of RAM's torsional data based on the drift only cases

# TODO: Think through importing when
#  a) A file has already been imported
#  b) The file location changes
#  c) The number of stories changes
#  d) The control points change
class RamDriftImporter:
    """A class that imports and parses drift output from RAM Structural
    System's Frame module. This class requires control points to have
    been set in RAM Frame."""

    def __init__(self, import_file_path=None) -> None:
        # self.import_file_path = import_file_path
        self.set_import_file_path(import_file_path)
        self.data = None
        # Indexes for the section dividers of the data array
        self.results_title_index = None
        self.load_cases_title_index = None
        self.torsional_title_index = None
        # Data containers for the parsed data
        self.load_cases = {}
        self.drift_data = {}
        self.drift_data_stories = []
        self.torsion_data = {}
        self.stories = []
        self.story_heights = {}
        self.total_height = None
        # Seismic Data
        self.importance_factor = None
        self.drift_amp_factor = None
        self.allowable_drift_limit = None
        # Automatically run the parser if an input file is given
        if self.import_file_path and os.path.exists(self.import_file_path):
            self.first_import()
            # self.import_drift_data()
            # self.parse_data()
            # self.set_stories()
            # return (self.load_cases, self.drift_data, self.torsion_data)

    # Importing Data Section
    def import_drift_data(self) -> None:
        """Imports the raw data csv file from RAM and stores the data
        in an arrary 'self.data'"""
        with open(self.import_file_path, "r") as file:
            reader = csv.reader(file)
            self.data = [row for row in reader]

    def set_import_file_path(self, filepath) -> bool:
        if filepath and os.path.exists(filepath):
            self.import_file_path = filepath
            return True
        else:
            self.import_file_path = None
            return False

    def first_import(self) -> None:
        """Imports data from current import_file, parses data,
        and sets stories.
        """

        self.import_drift_data()
        self.parse_data()
        self.set_stories()

    def reimport(self) -> None:
        """Re-imports data from current import_file"""

        self.import_drift_data()
        self.parse_data()
        if not self.check_stories():
            self.set_stories()
            self.wipe_story_heights()

    # Parsing Data Section
    def get_section_indexes(self) -> None:
        """Gets the indexes of the 'LOAD CASE DEFINITIONS', 'RESULTS', and
        TORSIONAL IRREGULARITY DATA' sections headers."""

        self.results_title_index = None
        self.load_cases_title_index = None
        self.torsional_title_index = None
        for i, row in enumerate(self.data):
            if row[0] == "LOAD CASE DEFINITIONS:":
                self.load_cases_title_index = i

            if row[0] == "RESULTS:":
                self.results_title_index = i

            if row[0] == "TORSIONAL IRREGULARITY DATA:":
                self.torsional_title_index = i

    def get_load_cases(self) -> None:
        self.load_cases = {}
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

    def parse_drift_data(self) -> None:
        self.drift_data = {}
        self.drift_data_stories = []

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
                # TODO This could be more efficient by putting one variable that is set to false if
                # the current story is the first story in the set ie has it come to its first repeat
                # TODO should this make a data type that has the story name, its story height and the total height
                if story not in self.drift_data_stories:
                    self.drift_data_stories.append(story)

            # Checks to see if the row is a drift load case. If so it adds the
            # data to the control point
            if row[1].strip() in self.load_cases:
                load_case = row[1].strip()
                displacement = [float(x) for x in row[2:4]]
                story_drift = [float(x) for x in row[4:6]]
                drift_ratio = [float(x) for x in row[6:]]

                max_displacement = max([abs(el) for el in displacement])
                max_story_drift = max([abs(el) for el in story_drift])

                data = {}
                data["displacement"] = displacement
                data["max_displacement"] = max_displacement
                data["story_drift"] = story_drift
                data["max_story_drift"] = max_story_drift
                data["drift_ratio"] = drift_ratio

                control_point_data["drifts"][story][load_case] = data

        # Adds the final control point to the drift data
        self.drift_data[control_point_name] = control_point_data

    def parse_torsional_data(self) -> None:
        """Parses the 'Torsional Irregularity Data from the input file"""
        self.torsion_data = {}
        axis = None
        for i in range(self.torsional_title_index + 1, len(self.data)):
            row = self.data[i]
            if "-Axis" in row[0]:
                if axis:
                    self.torsion_data[axis] = axis_dict
                axis = row[0][:-1]
                axis_dict = {}
                skip = 2
                continue

            # Skips the header line and the units lines
            if skip:
                # print("skip", skip)
                skip -= 1
                continue

            story = row[0]
            load_case = row[1].strip()

            # Check is the load case is not a drift case. If it is not a
            #  drift case then the data is not valid
            if (load_case != "-") and (load_case not in self.load_cases):
                # print("breaking at: |", load_case, "|")
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

    def parse_data(self) -> None:
        self.get_section_indexes()
        self.get_load_cases()
        self.parse_drift_data()
        self.parse_torsional_data()

    def parse_stories(self) -> None:
        stories = []
        for cp in self.drift_data:
            for story in self.drift_data[cp]["drifts"].keys():
                stories.append(story)
            return stories

    def set_stories(self) -> List[str]:
        """Set the stories by parsing the drift data.

        self.stories = self.parse_stories()
        """

        self.stories = self.parse_stories()

    def check_stories(self) -> bool:
        """Checks if the current stories list is equal to the stories
        in the current drift data.

        Returns True if the stories match. False otherwise
        """

        if self.stories == self.parse_stories():
            return True
        else:
            return False

    def wipe_story_heights(self) -> None:
        self.story_heights = {}
        self.total_height = None

    # Output Data Section
    def get_all_output(self) -> dict:
        return (self.load_cases, self.drift_data, self.torsion_data)

    def get_torsional_output(self) -> dict:
        return self.torsion_data

    def get_load_cases_output(self) -> dict:
        return self.load_cases

    def get_drift_output(self) -> dict:
        return self.drift_data

    def get_stories(self) -> List[str]:
        return self.stories

    # Print Data Section

    # This function isn't currently all that useful. It prints too much
    # data and the data is too messy to read. Consider a better way to
    # handle this. Also consider if this is necessary.
    def print_data(self) -> None:
        print("\nLoad Cases:\n")
        print(self.load_cases)
        print("\nDrift Data\n")
        print(self.drift_data)
        print("\nTorion Data\n")
        print(self.torsion_data)

    def print_Ax_values(self) -> None:
        """Prints the torsional amplification values (Ax) by story for
        each axis"""
        if self.torsion_data:
            for axis in self.torsion_data:
                print("\nAxis: ", axis)
                for story in self.torsion_data[axis]:
                    print(f"{story}: Ax=", self.torsion_data[axis][story]["Ax"])
        else:
            print(
                "\nTorsion Data Not Available. Import a csv file with drift only cases.\n"
            )

    # Set Functions Section

    def set_story_heights(self, height_dict) -> None:
        """Sets the story heights"""

        self.story_heights = height_dict
        self.set_total_height()

    def set_total_height(self):
        self.total_height = 0
        for story in self.story_heights:
            self.total_height += self.story_heights[story]

    def get_overall_heights(self):
        overall_heights = {}
        height = 0
        # print(self.story_heights)
        for i in range(len(self.stories) - 1, -1, -1):
            story = self.stories[i]
            height += self.story_heights[story]
            overall_heights[story] = height

        return overall_heights

    def set_drift_limits(self):
        self.drift_limits = {}
        # wind_total_drift_limit = self.total_height * 12 / 500
        # self.drift_limits["wind_total"] = wind_total_drift_limit
        overall_heights = self.get_overall_heights()
        for story in self.story_heights:
            # Initialize drift_limits per story
            self.drift_limits[story] = {}
            height = overall_heights[story]

            wind_limit = height * 12 / 500
            self.drift_limits[story]["wind"] = wind_limit

            # print(f"{story}: {wind_limit} in")

    def drift_ultilization(self):
        for cp in self.drift_data:
            for story, load_case_dict in self.drift_data[cp]["drifts"].items():
                # print(story, load_case)
                for load_case, data_dict in load_case_dict.items():
                    if load_case[0] == "W":
                        overall_wind_limit = self.drift_limits[story]["wind"]
                        displacement = data_dict["max_displacement"]
                        util = displacement / overall_wind_limit
                        print(cp, story, load_case, util)


# def wind_


def main():
    drift_importer = RamDriftImporter(FILE_PATH)

    # Print All Data
    # drift_importer.print_data()

    # Print Stories
    print(drift_importer.drift_data_stories)

    # output = drift_importer.get_all_output()
    # output = drift_importer.get_torsional_output()
    # drift_importer.print_Ax_values()
    # drift_importer.set_story_heights()
    # drift_importer.set_drift_limits()
    # print(drift_importer.torsion_data)
    # print(output)
    # for axis in output:
    #     print(output[axis])

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
                    max_displacement: val,
                    story_drift: [],
                    max_story_drift: val,
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

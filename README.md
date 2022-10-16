# ram-drift-parser

Copyright (c) 2022 Paul Numbers

This module parses RAM drift csv files, anaylzes the data, and presents applicable drift utilization and Ax values to facillate quick interation of RAM lateral models.

## Current Status: Pre-Alpha

This project is a work in progress.

As such, major functionality is currently being developed. See the development goals below for more information.

## How to Use

<!-- ### GUI -->

1. Run RAM Structural System's Frame module and switch the output format to text. This will produce CSV files instead of the default PDF viewer. Click the "Drift at Control Points" function and save the CSV data file somewhere convenient.

2. Run the drift_parser_gui.py module. This will bring up a GUI for using the drift_parser.

3. Click the "Import RAM File" button to load in the RAM CSV file from step 1.

4. Click the "Update Drift" button to load in the drift data.

5. Use the available information to inform your next iteration of the lateral design of the RAM structural model. Once this is complete, export the latest drift CSV file, click "Refresh RAM Data", and then click "Update Drift".

6. Repeat Step 5 until the Lateral Drifts are satisfactory.

## Primary Python Modules

The main python modules are:
- drift_parser.py
- drift_parser_gui.py
- drift_parser_cmd_line.py

The primary analysis module is the drift_parser.py. This module contains main importer class that does all the heavy lifting of importing and analyzing the csv RAM data.

The remaining modules are GUI and command line UI's to support the use of the drift_parser module.

# Current Development Goals

- Drift Utilization
    - Calculate and display the drift utilization for each load case
    - Display a window with the controlling load case and utilization ratio for each story
- Auto-load drift data upon import/refresh data
- Quick look up of drift data based on story and load case

# Legal

I, Paul Numbers, take no resposibility for the use of this software. All structural engineering for structures is to be done per the codes of the applicable jurisdiction within which the structures reside. The structural engineer utilizing this tool takes full resposibility for how this software is used in the design of a structure.
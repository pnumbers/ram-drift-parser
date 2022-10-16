# ram-drift-parser

Copyright (c) 2022 Paul Numbers

This module parses RAM drift csv files, anaylzes the data, and presents applicable drift utilization and Ax values to facillate quick interation of RAM lateral models.

## Current Status: Work-in-Progress

This project is a work in progress. 

## Primary Python Modules

The main python modules are:
- drift_parser.py
- drift_parser_gui.py
- drift_parser_cmd_line.py

The primary analysis module is the drift_parser.py. This module contains main importer class that does all the heavy lifting of importing and analyzing the csv RAM data.

The remaining modules are GUI and command line UI's to support the use of the drift_parser module.


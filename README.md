# Virtual_navigation_IBO2018
============================

dependencies:
os, scipy, numpy, fast_histogram, json , tkinter, matplotlib, sys , string , random , time , tendo

Contents:
---------
IBO_pre_GUI.py
Runs the somatosensory experiment. This is not logged. Multiple instances can be run. Easy. For showcasing purpouses.

IBO_main_GUI.py 'username'    (quotes are not needed, username is specified by the user. e.g. competitor1)
Runs the main single window GUI for the competition. Only one instance can run at the same time (tendo package).
First, it loads the cell firing and animal trajectory data from the Data/experiment1.mat.
Creates log files in the Log directory for each user:
    -username.log contains the actions of the user (starting the program, adding an answer).
    -username.json contains the current state of the practical: number of remaining tries, good answers, generated code

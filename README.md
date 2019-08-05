# Virtual_navigation_IBO2018
----------------------------
This script was the neurophysiology practical part of the International Biology Olympiad in Hungary, Szeged, 2019
----------------------------
dependencies:
os, scipy, numpy, fast_histogram, json , tkinter, matplotlib, sys , string , random , time , tendo

Contents:
---------
IBO_pre_GUI.py
Runs the somatosensory experiment. This is not logged. Multiple instances can be run. Easy. For showcasing purposes.

IBO_main_GUI.py 'username'    (quotes are not needed, username is specified by the user. e.g. "python IBO_main_GUI.py competitor1")
Runs the main single window GUI for the competition. Only one instance can run at the same time (tendo package).

This script loads the cell firing and animal trajectory data from the Data/experiment1.mat (this takes several seconds). Changing this file changes the order of the answers. Alternative datafiles can be found on the following link: https://drive.google.com/open?id=1XFForNUu6tOo5efuJKB-eoEkff57j9Tq

Creates log files in the Log directory for each user:

-username.log contains the actions of the user (starting the program, adding an answer). This can be useful to track the steps of the competitor if something funny happens.

-username.json contains the current state of the practical: number of remaining tries, good answers, generated code. This log file is instrumental to continue the experiment if the competitor accidentally quits from the program.

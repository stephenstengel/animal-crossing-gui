# Makefile for Animal Crossing GUI
# Creates a folder containing the exe and associated files needed to run
# the animal sorting program.
#
# Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#
# Will probably only work on Mac and Linux. No idea if Windows has Make.

sorter-gui:
	pyinstaller sorter-gui.py --windowed --add-data="settings.ini:." --add-data="checkpoint:checkpoint"

#Comment the above and use this one instead on windows:
#sorter-gui:
#	pyinstaller sorter-gui.py --windowed --add-data="settings.ini;." --add-data="checkpoint;checkpoint"

cmd:
	pyinstaller cmdsorting.py --distpath=cmddist --workpath=cmdbuild --add-data="settings.ini:." --add-data="checkpoint:checkpoint"



#This will not work on windows.
.PHONY: clean
clean:
	rm -rf dist build test-outputs/*/*.jpg  test-outputs/*  *.spec  cmddist  cmdbuild

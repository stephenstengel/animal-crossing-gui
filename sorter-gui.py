#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  sorter-gui.py
#
#  GUI for calling the tensorflow based animal picture sorter.
#  
#  Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#  


from tkinter import *
from tkinter import ttk

import os
import sys

from SorterWindow import SorterWindow


def main(args):
	print("Welcome to the animal crossing project animal sorter thing!")

	settingsFileName = "settings.ini"
	checkForSettingsFile(settingsFileName)

	root = Tk()
	SorterWindow(root)
	root.mainloop()
	
	return 0


def checkForSettingsFile(settingsFileName):
	print("settingsFileName: " + str(settingsFileName))
	if not os.path.isfile(os.path.normpath(settingsFileName)):
		print("Settings file not found!")
		sys.exit(1) ########################### Change this to an error popup + exit


if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))

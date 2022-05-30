#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  
#  Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#  

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import multiprocessing


def main(args):
	print("Hello! Loading...")
	
	#Splash screen should go here.
	#I can't find any working tutorials or documentation. Gtk.main()
	
	#My plan:
	#Create a splash window using default glade splash window thing
	#Create a timer like in handlers.
	#Use multiprocessing to spawn a function that does loading
	#check if it is done with the timer
	#when it is done, destroy the splash screen and load the main screen.
	
	print("loading file window...")
	from FileSelectWindow import FileSelectWindow
	
	print("Done!")
	# ~ splash.destroy()
	

	theWindow2 = FileSelectWindow()
	Gtk.main()

	return 0

if __name__ == '__main__':
	multiprocessing.freeze_support()
	import sys
	sys.exit(main(sys.argv))

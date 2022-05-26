#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  
#  Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#  
#  

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from FileChooser import FileChooser
from AnimalSorter import sortAnimalsIntoFolders

import time


class Handlers():
	def __init__(self, source_text_field, destination_text_field, progress_spinner):
		self.source_text_field = source_text_field
		self.destination_text_field = destination_text_field
		self.progress_spinner = progress_spinner
	
	def button_source_onclick(self, button):
		print("Source button clicked!")
		testChooser = FileChooser("Choose a source folder!")
		pathString = testChooser.pathStr
		print("Selected folder: " + str(pathString))
		if pathString is not None:
			self.source_text_field.set_text(pathString)
	
	def button_destination_clicked(self, button):
		print("Destination button clicked!")
		testChooser = FileChooser("Choose a destination folder!")
		pathString = testChooser.pathStr
		print("Selected folder: " + str(pathString))
		if pathString is not None:
			self.destination_text_field.set_text(pathString)
	
	
	#Need to add a check to make sure fields are not empty
	#maybe here, maybe in the sorter. Here makes sense because this can
	#get called over and over automatically. And make a popup error
	#message.
	def button_run_clicked(self, button):
		print("Run button clicked!")
		startTime = time.time()
		sourceStr = self.source_text_field.get_text()
		destStr = self.destination_text_field.get_text()
		if sourceStr == "":
			print("SOURCE STRING NULL!")
			print("\a")
		elif destStr == "":
			print("DEST STRING NULL!")
			print("\a")
		else:
			print("Sorting...")
			self.progress_spinner.start()
			sortAnimalsIntoFolders(sourceStr, destStr)
			print("Done!")
			self.progress_spinner.stop()
		endTime = time.time()
		print("That took: " + str(endTime - startTime) + " seconds.")

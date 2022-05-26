#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  
#  Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#  
#  

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from FileChooser import FileChooser

import multiprocessing


#global variable to kill a sorting process if the user clicks the exit button.
globalSortingProcess = None


class Handlers():
	isSortingHappening = False
	sortingProcess = None
	timeout_id = None
	
	def __init__(self, 
			source_text_field, 
			destination_text_field, 
			progress_bar,
			run_button):
		self.source_text_field = source_text_field
		self.destination_text_field = destination_text_field
		self.progress_bar = progress_bar
		self.run_button = run_button
	
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
		sourceStr = self.source_text_field.get_text()
		destStr = self.destination_text_field.get_text()
		if sourceStr == "":
			print("SOURCE STRING NULL!")
			print("\a")
		elif destStr == "":
			print("DEST STRING NULL!")
			print("\a")
		elif self.sortingProcess is None:
			from AnimalSorter import sortAnimalsIntoFolders #import lol
			print("Sorting...")
			self.sortingProcess = multiprocessing.Process(target=sortAnimalsIntoFolders, args=(sourceStr, destStr, self.progress_bar,))
			global globalSortingProcess
			globalSortingProcess = self.sortingProcess ## Tre grava amikoj! Always update together
			
			self.sortingProcess.start()
			self.start_timer()
			self.progress_bar.pulse()
			self.progress_bar.set_text("Processing...")
			self.progress_bar.set_show_text(True)
			self.run_button.set_sensitive(False)
			

	def myDestroy(self):
		global globalSortingProcess
		if globalSortingProcess is not None:
			if globalSortingProcess.is_alive():
				globalSortingProcess.terminate()
		
	
	def start_timer(self):
		self.timeout_id = GLib.timeout_add(1000, self.on_timeout, None)


	def stop_timer(self):
		if self.timeout_id:
			GLib.source_remove(self.timeout_id)
			self.timeout_id = None

	#This will check the status of the sorting process.
	#Reactivate button if done, else, pulse the progress bar.
	def on_timeout(self, *args, **kwargs):
		if self.timeout_id is not None:
			#Check if process is still running
			if self.sortingProcess is not None:
				if self.sortingProcess.is_alive():
					self.progress_bar.pulse()
				else:
					self.stop_timer()
				
					#reset the progress bar?
					self.progress_bar.set_fraction(0.0)
					self.progress_bar.set_text("Done!")
					self.progress_bar.set_show_text(True)
					
					#Set the run button back to clickable
					self.run_button.set_sensitive(True)
					
					self.sortingProcess = None
					global globalSortingProcess
					globalSortingProcess = self.sortingProcess #always update together.
				
			return True
		else:
			return False

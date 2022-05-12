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


class Handlers():
	def __init__(self, source_text_field, destination_text_field):
		self.source_text_field = source_text_field
		self.destination_text_field = destination_text_field
	
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
		
	def button_run_clicked(self, button):
		print("Run button clicked!")

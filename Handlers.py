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


class Handlers():
	def __init__(self):
		pass
	
	def button_source_onclick(self, button):
		print("Source button clicked!")
	
	def button_destination_clicked(self, button):
		print("Destination button clicked!")
		
	def button_run_clicked(self, button):
		print("Run button clicked!")

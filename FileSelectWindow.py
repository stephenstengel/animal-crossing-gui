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


from Handlers import Handlers


class FileSelectWindow(Gtk.Window):
	def __init__(self):
		super().__init__(title = "Animal Crossing File Classification")

		builder = Gtk.Builder()
		builder.add_from_file("file-select-window.glade")
		
		source_button = builder.get_object("source_button")
		destination_button = builder.get_object("destination_button")
		run_button = builder.get_object("run_button")
		
		
		window = builder.get_object("file_select_window")
		window.connect("destroy", Gtk.main_quit)

		myHandlers = Handlers()
		builder.connect_signals(myHandlers)
		
		window.show_all()

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
		source_text_field = builder.get_object("source_text_field")
		destination_text_field = builder.get_object("destination_text_field")
		progress_spinner = builder.get_object("progress_spinner")
		progress_bar = builder.get_object("progress_bar")
		
		
		window = builder.get_object("file_select_window")
		window.connect("destroy", Gtk.main_quit)
		window.connect("destroy", Handlers.myDestroy)

		myHandlers = Handlers(source_text_field, destination_text_field, progress_spinner, progress_bar)
		builder.connect_signals(myHandlers)
		
		window.show_all()

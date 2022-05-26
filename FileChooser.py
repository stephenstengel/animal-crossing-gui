#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class FileChooser():
	def __init__(self, titleText):
		self.pathStr = None #Stores the returned path.
		self.titleText = titleText

		#Sets up a file chooser dialog window object.
		dialog = Gtk.FileChooserDialog( \
				self.titleText, \
				None, \
				Gtk.FileChooserAction.SELECT_FOLDER, \
				(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		#Opens the dialog, waits for the return value.
		response = dialog.run()

		#Only save the path if the user clicked OK and not cancel.
		if response == Gtk.ResponseType.OK:
			self.pathStr = dialog.get_filename()

		#Close the dialog.
		dialog.destroy()


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
		self.pathStr = None
		self.titleText = titleText

#maybe the below should be in a function for clarity?

		dialog = Gtk.FileChooserDialog(self.titleText, None,
			Gtk.FileChooserAction.SELECT_FOLDER,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			self.pathStr = dialog.get_filename()

		dialog.destroy()


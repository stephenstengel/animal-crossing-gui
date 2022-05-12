#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  
#  Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#  


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from FileSelectWindow import FileSelectWindow


def main(args):
	print("hello")
	
	theWindow = FileSelectWindow()
	Gtk.main()

	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))

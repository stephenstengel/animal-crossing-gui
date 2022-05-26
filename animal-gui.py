#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  
#  Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#  

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def main(args):
	print("Hello! Loading...")
	
	#Splash screen should go here.
	#I can't find any working tutorials or documentation. Gtk.main()
	#makes the window show, BUT blocks execution until you close the splash window.

	# ~ splash = Gtk.Window(title="Hello World")
	# ~ splash.connect("destroy", Gtk.main_quit)
	
	# ~ splash.show_all()
	
	# ~ while Gtk.events_pending():
		# ~ Gtk.main_iteration()
	# ~ splash.show_all()
	# ~ splash.show()
	# ~ Gtk.main_iteration()
	

	#testing opening another window after doing some heavy imports.
	# ~ print("loading tensorflow...")
	# ~ import tensorflow as tf
	# ~ print("loading sklearn...")
	# ~ import sklearn
	# ~ print("loading skimage...")
	# ~ import skimage
	# ~ print("loading numpy...")
	# ~ import numpy as np
	# ~ print("loading keras.models...")
	# ~ from keras.models import Sequential
	# ~ print("loading inceptionv3...")
	# ~ from keras.applications.inception_v3 import InceptionV3
	# ~ print("loading keras layers...")
	# ~ from keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
	# ~ print("loading keras loss...")
	# ~ from keras.losses import SparseCategoricalCrossentropy
	
	# ~ print("Loading tensorflow...")
	# ~ import tensorflow
	
	print("loading file window...")
	from FileSelectWindow import FileSelectWindow
	
	print("Done!")
	# ~ splash.destroy()
	

	theWindow2 = FileSelectWindow()
	Gtk.main()

	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))

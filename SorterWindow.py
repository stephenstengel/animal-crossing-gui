#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  SorterWindow.py
#
#  GUI for calling the tensorflow based animal picture sorter.
#  
#  Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#  


from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import os

from functools import partial

from AnimalSorter import sortAnimalsIntoFolders

#Heavy influence from the tutorial at:  https://tkdocs.com/tutorial/firstexample.html


STEPHEN_DEBUG = True

class SorterWindow:
	sourceStr = None
	sourceStr_entry = ""
	destStr = None
	destStr_entry = ""
	mainframe = None
	

	def __init__(self, root):
		root.title("Animal Sorter!")

		self.mainframe = ttk.Frame(root, padding="10 10 10 10")
		self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)

		self.sourceStr = StringVar()
		self.sourceStr_entry = ttk.Entry(self.mainframe, width=100, textvariable=self.sourceStr)
		self.sourceStr_entry.grid(column=2, row=1, sticky=(W, E))

		self.destStr = StringVar()
		self.destStr_entry = ttk.Entry(self.mainframe, width=100, textvariable=self.destStr)
		self.destStr_entry.grid(column=2, row=2, sticky=(W, E))

		# ~ ttk.Button(self.mainframe, text="Source Folder", command=self.openSourceDialog).grid(column=3, row=1, sticky=W)
		sourceTitle = "Choose a source folder..."
		sourceCommand = partial(self.openFolderDialog, self.sourceStr, sourceTitle)
		ttk.Button(self.mainframe, text="Source Folder", command = sourceCommand).grid(column=3, row=1, sticky=W)
		
		destTitle = "Choose a destination folder..."
		destCommand = partial(self.openFolderDialog, self.destStr, destTitle)
		ttk.Button(self.mainframe, text="Destination Folder", command = destCommand).grid(column=3, row=2, sticky=W)
		
		ttk.Button(self.mainframe, text="Run Sorter", command=self.testFunction).grid(column=2, row=3, sticky=W)
		
		#Add a little padding to each widget
		for child in self.mainframe.winfo_children(): 
			child.grid_configure(padx=5, pady=5)

		if STEPHEN_DEBUG:
			self.sourceStr.set(os.path.normpath("/home/stephen/Documents/School/0spring22/animal-crossing/animal-crossing-gui/test-images"))
			self.destStr.set(os.path.normpath("/home/stephen/Documents/School/0spring22/animal-crossing/animal-crossing-gui/test-outputs"))


	def openFolderDialog(self, thisStr, thisTitle, *args):
		thisStr.set(filedialog.askdirectory(title = thisTitle))
		
	
	# ~ def runSorting

	def testFunction(self, *args):
		try:
			print("Test function!")
		except ValueError:
			pass



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

from AnimalSorter import sortAnimalsIntoFolders

#Heavy influence from the tutorial at:  https://tkdocs.com/tutorial/firstexample.html


class SorterWindow:
	def __init__(self, root):
		root.title("Animal Sorter!")

		mainframe = ttk.Frame(root, padding="10 10 10 10")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)

		sourceStr = StringVar()
		sourceStr_entry = ttk.Entry(mainframe, width=100, textvariable=sourceStr)
		sourceStr_entry.grid(column=2, row=1, sticky=(W, E))

		destStr = StringVar()
		destStr_entry = ttk.Entry(mainframe, width=100, textvariable=destStr)
		destStr_entry.grid(column=2, row=2, sticky=(W, E))

		ttk.Button(mainframe, text="Source Folder", command=self.testFunction).grid(column=3, row=1, sticky=W)
		ttk.Button(mainframe, text="Destination Folder", command=self.testFunction).grid(column=3, row=2, sticky=W)
		ttk.Button(mainframe, text="Run Sorter", command=self.testFunction).grid(column=2, row=3, sticky=W)




	def testFunction(*args):
		print("Test function!")




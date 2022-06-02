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
from tkinter import messagebox
from tkinter import filedialog

import os
import threading
from functools import partial

from AnimalSorter import sortAnimalsIntoFolders

#Heavy influence from the tutorial at:  https://tkdocs.com/tutorial/firstexample.html


STEPHEN_DEBUG = False

class SorterWindow:
	#I like setting these here because they will cause error messages if something goes wrong. --Stephen
	sourceStr = None
	sourceStr_entry = ""
	destStr = None
	destStr_entry = ""
	mainframe = None
	myProgressBar = None
	myRunButton = None
	mySortThread = None
	waitTime = None

	def __init__(self, root):
		self.waitTime = 2000
		self.root = root
		self.root.title("Animal Sorter!")
		
		## Create menu
		m_help = Menu(self.root, tearoff=0)
		m_help.add_command(label="Instructions", command = lambda: self.root.event_generate("<<OpenInstructionsDialog>>"))
		m_help.add_command(label="About", command = lambda: self.root.event_generate("<<OpenAboutDialog>>"))
		self.root["menu"] = m_help
		self.root.bind("<<OpenInstructionsDialog>>", self.launchInstructions)
		self.root.bind("<<OpenAboutDialog>>", self.launchAbout)
		
		#Create the background frame
		self.mainframe = ttk.Frame(self.root, padding="10 10 10 10")
		self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

		#Set weights for resizing
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)

		self.mainframe.columnconfigure(0, weight=0)
		self.mainframe.rowconfigure(0, weight=0)
		self.mainframe.columnconfigure(1, weight=0) #note 0
		self.mainframe.rowconfigure(1, weight=1)
		self.mainframe.columnconfigure(2, weight=1)
		self.mainframe.rowconfigure(2, weight=1)
		self.mainframe.columnconfigure(3, weight=1)
		self.mainframe.rowconfigure(3, weight=1)

		#Create the text entry fields
		self.sourceStr = StringVar()
		self.sourceStr_entry = ttk.Entry(self.mainframe, width=80, textvariable=self.sourceStr)
		self.sourceStr_entry.grid(column=2, row=1, sticky=(W, E))

		self.destStr = StringVar()
		self.destStr_entry = ttk.Entry(self.mainframe, width=80, textvariable=self.destStr)
		self.destStr_entry.grid(column=2, row=2, sticky=(W, E))

		#Create the buttons
		sourceTitle = "Choose a source folder..."
		sourceCommand = partial(self.openFolderDialog, self.sourceStr, sourceTitle)
		ttk.Button(self.mainframe, text="Source Folder", command = sourceCommand).grid(column=3, row=1, sticky = W + E)
		
		destTitle = "Choose a destination folder..."
		destCommand = partial(self.openFolderDialog, self.destStr, destTitle)
		ttk.Button(self.mainframe, text="Destination Folder", command = destCommand).grid(column=3, row=2, sticky = W + E)
		
		self.myRunButton = ttk.Button(self.mainframe, text="Run Sorter", command=self.runSorting)
		self.myRunButton.grid(column=3, row=3, sticky = W + E)
		
		#Create progress bar
		self.myProgressBar = ttk.Progressbar(self.mainframe, orient=HORIZONTAL, length=200, mode= "indeterminate")
		self.myProgressBar.grid(column = 2, row = 3, sticky = W + E)
		
		#Add a little padding to each widget
		for child in self.mainframe.winfo_children(): 
			child.grid_configure(padx=5, pady=5)

		#Set default entry field texts
		if STEPHEN_DEBUG:
			self.sourceStr.set(os.path.normpath("/home/stephen/Documents/School/0spring22/animal-crossing/animal-crossing-gui/test-images"))
			self.destStr.set(os.path.normpath("/home/stephen/Documents/School/0spring22/animal-crossing/animal-crossing-gui/test-outputs"))
		else:
			self.sourceStr.set(os.path.normpath("Enter path to images to be sorted"))
			self.destStr.set(os.path.normpath("Enter path to folder where the sorted pictures will go."))


	#Open a popup for the about button.
	def launchAbout(*args):
		theMessage = "This program takes images in a folder and sorts " \
				"them into an output folder based on what animal the" \
				" machine learning algorithm thinks they are."
		theMessage += \
				"\n\nAnimal Crossing Project\n\n" \
				+ "CWU 2022\n\n" \
				+ "Adara Andonie\n" \
				"Alex Worland\n" \
				"Harlow Huber\n" \
				"Lincoln Huber\n" \
				"Stephen Stengel\n"
		
		messagebox.showinfo(title = "About this program", message = theMessage)


	#Open a popup for the instructions button.
	def launchInstructions(*args):
		theMessage = "Click the \"Source Folder\" button to choose what folder of pictures to sort.\n\n" \
				"Then click the \"Destination Folder\" button to choose where to copy the sorted pictures to.\n\n" \
				"Then click the \"Run Sorter\" button to perform the sorting."
		messagebox.showinfo(title = "Instructions", message = theMessage)


	def openFolderDialog(self, thisStr, thisTitle, *args):
		thisStr.set(filedialog.askdirectory(title = thisTitle))
		
	
	def runSorting(self, *args):
		source = self.sourceStr.get()
		dest = self.destStr.get()
		
		#check if either empty
		if source == "":
			print("source empty! Make a popup to inform them!")
		
			return
		elif dest == "":
			print("Dest empty! Make popup!")
			
			return
		
		#check if strings are the same
		elif source == dest:
			print("source == dest. Make popup for this as well!")
		
			return
		
		#run the function
		
		self.myProgressBar.start()
		self.myRunButton.state(["disabled"])
		
		if STEPHEN_DEBUG:
			self.mySortThread = threading.Thread(target = self.testFunction, args = (source, dest,))
		else:
			self.mySortThread = threading.Thread(target = sortAnimalsIntoFolders, args = (source, dest,))
		self.mySortThread.start()
		self.root.after(self.waitTime, self.threadChecker)


	#Check if the sorting thread is done every few seconds.
	def threadChecker(self):
		print("Threadchecker called!")
		if self.mySortThread.is_alive():
			self.root.after(self.waitTime, self.threadChecker)
		else:
			self.resetAfterComplete()


	def resetAfterComplete(self):
		self.myProgressBar.stop()
		self.mySortThread = None
		self.myRunButton.state(["!disabled"])
		print("reset complete")
		#create popup to say done?


	def testFunction(self, *args):
		try:
			print("Test function!")
			print("source: " + str(self.sourceStr.get()))
			print("dest: " + str(self.destStr.get()))
		except ValueError:
			pass



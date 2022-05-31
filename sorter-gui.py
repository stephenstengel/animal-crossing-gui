#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  sorter-gui.py
#
#  GUI for calling the tensorflow based animal picture sorter.
#  
#  Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#  


from tkinter import *
from tkinter import ttk

from SorterWindow import SorterWindow


def main(args):
	print("Welcome to the animal crossing project animal sorter thing!")
	
	root = Tk()
	SorterWindow(root)
	root.mainloop()
	
	return 0


if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))

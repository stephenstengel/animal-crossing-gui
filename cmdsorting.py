#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  
#  Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#  
# 

import os
import sys

from AnimalSorter import sortAnimalsIntoFolders

def main(args):
	print("Hello!")
	inStr, outStr = checkArgs(args)
	
	print("Running program...")
	sortAnimalsIntoFolders(inStr, outStr)
	print("Done!")
	
	return 0


def checkArgs(args):
	argslen = len(args)
	firstStr, secondStr = None, None
	if argslen == 1:
		print("No input. Using manual mode.")
		firstStr, secondStr = askForInput()
	if argslen == 2 and args[1] == "tux":
		printTux()
		sys.exit(99)
	elif argslen == 3:
		firstStr, secondStr = args[1], args[2]
	elif argslen > 3:
		print("Bad input")
		#print the helpfile and exit
		sys.exit(2)
	
	if firstStr is None or secondStr is None:
		print("a folder is still missing!")
		sys.exit(1)

	firstStr = os.path.normpath(firstStr)
	secondStr = os.path.normpath(secondStr)

	if firstStr != None and secondStr != None:
		print("Input folder: " + str(firstStr) + "\n" \
				+ "Output folder: " + str(secondStr) )

	return firstStr, secondStr


def askForInput():
	print("Enter the relative path of the input pictures folder...")
	inStr = input()
	print("Enter the relative path of where you would like the sorted pictures to be saved...")
	outStr = input()
	
	return inStr, outStr


def printTux():
	with open("tux.ascii", "r") as tuxFile:
		for line in tuxFile:
			print(line, end = "")
		print()

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))

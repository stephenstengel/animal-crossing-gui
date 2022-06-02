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

HELPFILE_PATH = "cmd-helpfile.txt"


def main(args):
	print("Hello!")
	inStr, outStr = checkArgs(args)
	
	print("Running program...")
	sortAnimalsIntoFolders(inStr, outStr)
	print("Done!")
	
	return 0


def checkArgs(args):
	helpArgs = ["--help", "-help", "help", "h", "-h", "--h"]
	if not set(helpArgs).isdisjoint(args):
		printHelpFile()
		sys.exit(-4)

	argslen = len(args)
	firstStr, secondStr = "", ""
	
	if argslen == 1:
		print("No input. Using manual mode. (Press control + C to exit...")
		firstStr, secondStr = askForInput()
	elif argslen == 2 and args[1] == "tux":
		printTextFile("tux.ascii")
		sys.exit(99)
	elif argslen == 3:
		firstStr, secondStr = args[1], args[2]
	elif argslen > 3:
		print("Bad input")
		printHelpFile()
		sys.exit(2)
	
	if firstStr == "" or secondStr == "":
		print("a folder is still not specified!")
		sys.exit(1)

	firstStr = os.path.abspath(firstStr)
	secondStr = os.path.abspath(secondStr)

	if firstStr != "" and secondStr != "":
		print("Input folder: " + str(firstStr) + "\n" \
				+ "Output folder: " + str(secondStr) )

	return firstStr, secondStr


def askForInput():
	print("Enter the path of the input pictures folder...")
	inStr = input()
	print("Enter the path of where you would like the sorted pictures to be saved...")
	outStr = input()
	
	return inStr, outStr


def printTextFile(fileName):
	with open(fileName, "r") as tuxFile:
		for line in tuxFile:
			print(line, end = "")
		print()

def printHelpFile():
	printTextFile(HELPFILE_PATH)

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))

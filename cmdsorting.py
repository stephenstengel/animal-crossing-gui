#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  
#  Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#  
# 

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
		# ~ firstStr, secondStr = askForInput()
	if argslen == 3:
		firstStr, secondStr = args[1], args[2]
	if firstStr != None and secondStr != None:
		print("Input folder: " + str(firstStr) + "\n" 
				+ "Output folder: " + str(secondStr) )
	# ~ askIfCorrect()
	#while loop to keep asking for the input and output folders until the user types them correctly.
	
	if argslen == 2 or argslen > 3:
		pass
		#print the helpfile and exit
		exit(2)
	
	if firstStr is None or secondStr is None:
		print("Testing exit!")
		print("a string is still none!")
		exit(1)

	return firstStr, secondStr

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))

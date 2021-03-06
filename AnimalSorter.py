#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  animal-sorter.py
#
#  Sorts the animal pictures into folders based on a trained tensorflow model.
#  
#  Copyright 2022 Stephen Stengel <stephen.stengel@cwu.edu> and friends
#  


import os

#Not currently needed. We load a saved version of the whole model.
#We would need this if we switched to loading weights
# ~ from models import currentBestModel

CLASS_NAMES_LIST_INT = []
CLASS_NAMES_LIST_STR = []

IMG_WIDTH = None
IMG_HEIGHT = None
IMG_CHANNELS = None
IMG_SHAPE_TUPPLE = (IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)
BATCH_SIZE = None
CHECKPOINT_FOLDER = None

DEBUG_MODE = False


def sortAnimalsIntoFolders(sourceStr, destStr):
	import time
	
	settingsFileName = os.path.normpath("settings.ini")
	settingsDict = getSettingsFromFile(settingsFileName)
	updateGlobalsFromSettings(settingsDict)
	
	if DEBUG_MODE:
		print("Settings retrieved from " + settingsFileName)
		print("IMG_WIDTH: " + str(IMG_WIDTH))
		print("IMG_HEIGHT: " + str(IMG_HEIGHT))
		print("IMG_CHANNELS: " + str(IMG_CHANNELS))
		print("BATCH_SIZE: " + str(BATCH_SIZE))
		print("CHECKPOINT_FOLDER: " + str(CHECKPOINT_FOLDER))
	
	print("Source dir: " + str(sourceStr))
	print("Destenation dir: " + str(destStr))
	
	#create the folder structure within the destination directory.
	print("Setting up output directories...")
	foldersToCreate = createOutputFoldernames(CLASS_NAMES_LIST_STR, destStr)
	makeDirectories(foldersToCreate)
	
	
	#Turn the input images into a dataset?
	print("Loading the dataset...")
	startDataLoad = time.time()
	images_ds, originalFullNames = createDatasetFromImages(sourceStr)
	endDataLoad = time.time()
	print("Dataset loaded in " + str(round(endDataLoad - startDataLoad, 4)) + " seconds.")
	
	#normalize file paths for all operating systems
	originalFullNames = normalizeAllNames(originalFullNames)
	
	#strip base path from original names
	originalNames = stripBasepathFromFilenames(originalFullNames)
	

	#It might be faster to load the model and weights separately. need testing.
	#how to load the checkpoint weights separate from the model
	# ~ theModel.load_weights(os.path.abspath(CHECKPOINT_FOLDER))

	startModelLoadTime = time.time()
	print("Loading model...")
	from tensorflow.keras.models import load_model
	theModel = load_model(CHECKPOINT_FOLDER)
	theModel.summary()
	mLoadElapsed = time.time() - startModelLoadTime
	print("Loading model complete in: " + str(round(mLoadElapsed, 4)) + " seconds.")
	
	
	#Get a list of predictions
	print("Making predictions...")
	startTime = time.time()
	predictionsArray = theModel.predict( \
			images_ds,
			verbose = 1,
			)
	elapsedTime = time.time() - startTime
	print(str(predictionsArray))
	print("Prediction took: " + str(round(elapsedTime, 4)) + " seconds.")
	
	print("Copying files...")
	copyPredictions(originalFullNames, originalNames, predictionsArray, destStr, CLASS_NAMES_LIST_INT, CLASS_NAMES_LIST_STR)


#This function sets a bunch of settings from a file.
#Maybe the threading return value code could make a popup on error.
def getSettingsFromFile(settingsFileName):
	fileContents = []
	with open(settingsFileName, "r") as settingsFile:
		fileContents = settingsFile.readlines()
	
	#get only non comment lines
	goodContents = []
	for line in fileContents:
		if not line.startswith("#") and line != "\n":
			goodContents.append(line.rstrip())

	#convert to a dictionary
	settingsDict = {}
	for thing in goodContents:
		name, value = thing.split("=")
		settingsDict.update({name : value})
	
	if DEBUG_MODE:
		for thing in settingsDict:
			print(str(thing) + ": ", end="")
			print(settingsDict[thing])
	
	return settingsDict


def updateGlobalsFromSettings(settingsDict):
	##! BIG NOTE !##
	# The names of the items in this settingsDict dictionary are not
	# automatically the same as in the settings file. Take care to copy
	# paste them if you update this. There might be a clever way to
	# get the same name automatically.
	global IMG_WIDTH
	IMG_WIDTH = int(settingsDict["IMG_WIDTH"])
	global IMG_HEIGHT
	IMG_HEIGHT = int(settingsDict["IMG_HEIGHT"])
	global IMG_CHANNELS
	IMG_CHANNELS = int(settingsDict["IMG_CHANNELS"])
	global CHECKPOINT_FOLDER
	CHECKPOINT_FOLDER = settingsDict["CHECKPOINT_FOLDER"] #This one remains a string
	global BATCH_SIZE
	BATCH_SIZE = int(settingsDict["BATCH_SIZE"])
	
	#parse the class list
	rawClassNamesStr = settingsDict["classNames"]
	splitClassNamesList = rawClassNamesStr.split(",")
	
	global CLASS_NAMES_LIST_STR
	CLASS_NAMES_LIST_STR = splitClassNamesList
	
	#Not sure what I was thinking way back when I made CLASS_NAMES_LIST_INT in the loader haha.
	# ~ intsListLol = [x for x in range(len(splitClassNamesList))] #A little roundabout
	intsListLol = range(len(splitClassNamesList)) #Apparently equivalent.
	global CLASS_NAMES_LIST_INT
	CLASS_NAMES_LIST_INT = intsListLol
	
	if DEBUG_MODE:
		print("rawclassnamesstr: " + str(rawClassNamesStr))
		print("splitClassNamesList: " + str(splitClassNamesList))
		print("CLASS_NAMES_LIST_INT: " + str(CLASS_NAMES_LIST_INT))
		for thing in CLASS_NAMES_LIST_INT:
			print(thing)
			
		print("CLASS_NAMES_LIST_STR: " + str(CLASS_NAMES_LIST_STR))
		for thing in CLASS_NAMES_LIST_STR:
			print(thing)
		
		testBoi = range(100, 0, -1)
		print("testboi: " + str(testBoi))
		print("now tryina get just 5...")
		print("testBoi[5]: " + str(testBoi[5]))


def normalizeAllNames(originalFullNames):
	outList = []
	for name in originalFullNames:
		outList.append( os.path.normpath(name) )
	
	return outList


#This function copys the original full size image into the correct
#destination folder based on the result of the search.
def copyPredictions(originalFullNames, originalNames, predictionsArray, destStr, classNamesListInt, classNamesListStr):
	import shutil
	#Get predicted labels in integer form.
	labelsListInt = getPredictedLabels(predictionsArray)
	
	#get all predicted labels in string form for use as output folders
	labelsListStr = getAllOutFoldersStr(classNamesListStr, labelsListInt)
	
	for i in range(len(predictionsArray)):
		thisOutClassFolder = labelsListStr[i] #get this out folder
		thisOutName = originalNames[i]
		
		#get full path of output name
		thisOutputFolder = os.path.join(destStr, thisOutClassFolder)
		
		#copy original to destination
		thisFullOriginalName = originalFullNames[i]
		
		try:
			shutil.copy2( thisFullOriginalName, thisOutputFolder)
		except:
			print("copy skipping: " + str(thisName))







#Takes a list of file paths and returns a tensorflow dataset object.
		#Resize to the same size as the model was trained on.
#NOTE: If we instead load each image individually with: tf.keras.preprocessing.image.load_img()
#We can save them in a numpy array
#then we can use a for loop to predict on each image individually
#this way we can update a loading bar to show how much time is left.
#OR EVEN BETTER:
#To save ram on their shitty government workstations, we can load each
#image individually, and the predict that one image right away.
#That way there is only ever one image in ram. The downside is that there
#will probably be no batching or multiprocessing.? We'll have to test and see!
#OR we could combine the two methods:
#We could load BATCH_NUM images from files, and combine them into a numpy array,
#then predict on each image in the array and sort, then continue with
#the rest of the dataset in this way.
def createDatasetFromImages(sourceFolderStr):
	from tensorflow.keras.preprocessing import image_dataset_from_directory
	out_ds = image_dataset_from_directory( \
			sourceFolderStr,
			labels = None,
			label_mode = None,
			color_mode = "rgb",
			image_size = (IMG_HEIGHT, IMG_WIDTH), #triple check it is (h, w). Pillow files are (w, h) and need conversion to numpy/tensorflow by swapping height and width dimensions. (transpose?)
			batch_size = BATCH_SIZE, #this might need tweaking depending on how much ram their computers have. 32 is default.
			shuffle = False,
			interpolation = "bilinear", #default is bilinear
			)
	
	
	# Found undocumented filename return lol
	# https://stackoverflow.com/questions/62166588/how-to-obtain-filenames-during-prediction-while-using-tf-keras-preprocessing-ima
	# ~ fnames = out_ds.file_paths
	# ~ for name in fnames:
		# ~ print(name)
		
		
	outNames = out_ds.file_paths
	
	from tensorflow import data
	AUTOTUNE = data.AUTOTUNE
	
	try:
		from tensorflow.keras.layers import Rescaling
	except:
		from tensorflow.keras.layers.experimental.preprocessing import Rescaling

	normalization_layer = Rescaling(1./255) #for newer versions of tensorflow
	out_ds = out_ds.map(lambda x: normalization_layer(x),  num_parallel_calls=AUTOTUNE)
	
	
	return out_ds, outNames



def createOutputFoldernames(namesList, destStr):
	outFNames = []
	destNormalized = os.path.normpath(destStr)
	for name in namesList:
		outFNames.append( os.path.join(destNormalized, name) )
	
	return outFNames
	


# Creates the necessary directories.
def makeDirectories(listOfFoldersToCreate):
	for folder in listOfFoldersToCreate:
		if not os.path.isdir(folder):
			os.makedirs(folder)


#deletes each dir within a list
def deleteDirectories(listDirsToDelete):
	import shutil
	for folder in listDirsToDelete:
		if os.path.isdir(folder):
			shutil.rmtree(folder, ignore_errors = True)	



def sortPredictions(images_ds, predictionsArray, sourceStr, destStr, classNamesListInt, classNamesListStr):
	
	from skimage.io import imsave
	from skimage.util import img_as_ubyte
	import numpy as np
	
	#Get list of predictions in int form
	labelsListInt = getPredictedLabels(predictionsArray)

	#get list of output names given the input names using os.walk (without a base path)
	outNamesList = getListOfFilenames(sourceStr)
	
	#Put images in the correct places.
	i = 0
	for batch in images_ds:
		batchArr = np.asarray(batch) 
		while batchArr is not None: #HUHUHUHU
			for j in range(len(batchArr)):
				thisImg = img_as_ubyte( batchArr[j] )
				thisFolderStr = getOutFolderNameStr(classNamesListStr, labelsListInt[i])
				thisFileName = outNamesList[i]
				fnameStr = os.path.join(destStr, thisFolderStr, thisFileName)
				imsave(fnameStr, thisImg)
				i += 1
	
	# ~ for i in range(len(images_ds)):
		
	
	#could we do for i in range len(_ds) * batch_size .. for j in range len (_ds)??


def getAllOutFoldersStr(classNamesListStr, labelsListInt):
	outFoldersList = []
	for labelInt in labelsListInt:
		outFoldersList.append( getOutFolderNameStr(classNamesListStr, labelInt ) )
	
	return outFoldersList

def getOutFolderNameStr(classNamesListStr, classInt):
	return classNamesListStr[ classInt ]



#Returns a list of filenames from the input directory
def getListOfFilenames(baseDirectory, include_base = False):
	myNames = []
	for (root, dirNames, fileNames) in os.walk(baseDirectory):
		for aFile in  fileNames:
			if include_base:
				myNames.append( os.path.join( root, aFile ) )
			else:
				myNames.append(aFile)
	
	return myNames

def stripBasepathFromFilenames(inList):
	outList = []
	for name in inList:
		outList.append( os.path.basename(name) )

	return outList


#Transform scores array into predicted labels.
def getPredictedLabels(predictedScores):
	import numpy as np
	outList = []
	for score in predictedScores:
		outList.append(np.argmax(score))
	
	return np.asarray(outList)

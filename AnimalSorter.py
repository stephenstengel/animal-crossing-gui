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



# ~ from models import currentBestModel


#Current plan:
#start with making the sorting function work. 
#Add the funtion to the run button with default folder values for testing.

#Then:
#Open up a splash screen when user clicks on the exe
#Load up the imports required
#delete the splash screen with gtk.clear or something.
#load up the actual program window

#In the main window, use the file paths as the inputs to the sorting function.


CLASS_BOBCAT = 0
CLASS_COYOTE = 1
CLASS_DEER = 2
CLASS_ELK = 3
CLASS_HUMAN = 4
CLASS_NOT_INTERESTING = 5
CLASS_RACCOON = 6
CLASS_WEASEL = 7

CLASS_BOBCAT_STRING = "bobcat"
CLASS_COYOTE_STRING = "coyote"
CLASS_DEER_STRING = "deer"
CLASS_ELK_STRING = "elk"
CLASS_HUMAN_STRING = "human"
CLASS_RACCOON_STRING = "raccoon"
CLASS_WEASEL_STRING = "weasel"
CLASS_NOT_INTERESTING_STRING = "not"

CLASS_NAMES_LIST_INT = [CLASS_BOBCAT, CLASS_COYOTE, CLASS_DEER, CLASS_ELK, CLASS_HUMAN, CLASS_NOT_INTERESTING, CLASS_RACCOON, CLASS_WEASEL]
CLASS_NAMES_LIST_STR = [CLASS_BOBCAT_STRING, CLASS_COYOTE_STRING, CLASS_DEER_STRING, CLASS_ELK_STRING, CLASS_HUMAN_STRING, CLASS_NOT_INTERESTING_STRING, CLASS_RACCOON_STRING, CLASS_WEASEL_STRING]


## We really should make a config file so that we don't need all these globals. ##
IMG_WIDTH = 100
IMG_HEIGHT = 100
IMG_CHANNELS = 3
IMG_SHAPE_TUPPLE = (IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)

CHECKPOINT_FOLDER = os.path.normpath("./checkpoint/")
print("Checkpoint folder: " + CHECKPOINT_FOLDER)

#Testing print
PRESENT_DIRECTORY = os.path.normpath(os.path.dirname(__file__) )
print("Present directory: " + PRESENT_DIRECTORY)


def sortAnimalsIntoFolders(sourceStr, destStr):
	settingsFileName = os.path.normpath("settings.ini")
	settingsDict = getSettingsFromFile(settingsFileName)
	updateGlobalsFromSettings(settingsDict)
	
	
	print("img wid: " + str(IMG_WIDTH))
	print("img h: " + str(IMG_HEIGHT))
	print("img chan: " + str(IMG_CHANNELS))
	print("check: " + str(CHECKPOINT_FOLDER))
	
	# ~ print("testing exit(2)")
	# ~ import sys
	# ~ sys.exit(2)
	
	import time
	print("Source dir: " + str(sourceStr))
	print("Destenation dir: " + str(destStr))
	
	#create the folder structure within the destination directory.
	print("Setting up output directories...")
	foldersToCreate = createOutputFoldernames(CLASS_NAMES_LIST_STR, destStr)
	makeDirectories(foldersToCreate)
	
	#Load the model from models.py. This is currently blocking the gui. (can't update window till done)
	#maybe this should be a part of the splash screen step?
	#just pass the model in as a parameter.
	#maybe change this to a class object and save as a field.? more work tho.
	#another solution: a separate button to load the model, keep the run button disabled until it is readied.
	# ~ print("Loading model...")
	# ~ theModel = currentBestModel(IMG_SHAPE_TUPPLE)
	# ~ print("printing summary...")
	# ~ theModel.summary()
	
	#Load the checkpoint weights.
	# ~ print("Loading weights...")
	# ~ theModel.load_weights(os.path.abspath(CHECKPOINT_FOLDER))
	
	
	#Turn the input images into a dataset?
	print("Loading the dataset...")
	images_ds, originalFullNames = createDatasetFromImages(sourceStr)
	
	#normalize file paths for all operating systems
	originalFullNames = normalizeAllNames(originalFullNames)
	
	#strip base path from original names
	originalNames = stripBasepathFromFilenames(originalFullNames)
	
	

	#It might be faster to load the model and weights separately. need testing.
	startModelLoadTime = time.time()
	print("Loading model...")
	# ~ print("COMENTED OUT FOR TESTING!")
	from tensorflow.keras.models import load_model
	theModel = load_model(CHECKPOINT_FOLDER)
	theModel.summary()
	mLoadElapsed = time.time() - startModelLoadTime
	print("Loading model complete in: " + str(mLoadElapsed) + " seconds.")
	
	
	#Get a list of predictions
	print("Making predictions...")
	startTime = time.time()
	predictionsArray = theModel.predict( \
			images_ds,
			verbose = 1,
			# ~ steps = 2, #only predict two batches of 32 pictures to test faster.
			)
	elapsedTime = time.time() - startTime
	print(str(predictionsArray))
	print("Prediction took: " + str(elapsedTime) + " seconds.")
	
	
	print("Copying files...")
	copyPredictions(originalFullNames, originalNames, predictionsArray, destStr, CLASS_NAMES_LIST_INT, CLASS_NAMES_LIST_STR)
	print("Done!")


#This function sets a bunch of settings from a file.
#Maybe the threading return value code could make a popup on error.
def getSettingsFromFile(settingsFileName):
	print("settingsFileName: " + str(settingsFileName))
	import sys
	if not os.path.isfile(settingsFileName):
		print("Settings file not found!")
		sys.exit(3)
	
	fileContents = []
	with open(settingsFileName, "r") as settingsFile:
		print("file opened!")
		fileContents = settingsFile.readlines()
	
	for thing in fileContents:
		print(thing, end="")
	print()
	
	goodContents = []
	#get only non comment lines
	for line in fileContents:
		if not line.startswith("#") and line != "\n":
			print("setting detected")
			goodContents.append(line.rstrip())
		
	print("new contents...")
	for thing in goodContents:
		print(thing)
	print("### END LIST ###")
	
	settingsDict = {}
	for thing in goodContents:
		name, value = thing.split("=")
		print(str(name) + " " + str(value))
		settingsDict.update({name : value})
	
	for thing in settingsDict:
		print(thing, end=": ")
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
	



def normalizeAllNames(originalFullNames):
	outList = []
	for name in originalFullNames:
		outList.append( os.path.normpath(name) )
	
	return outList



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
			batch_size = 32, #this might need tweaking depending on how much ram their computers have. 32 is default.
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



#Need to preserve filenames with os.walk (thats how tensorflow loads them when not shuffled.)
#Investigate! Make sure that the images have the right names when they come out! A small class like weasel should be good for that.
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
#uses os.walk, so it should be the same order as tensorflow loads them!!!!!!!!!!!!!!!!!!!!!!!!!!!maybe
#Currently not getting the same filenames as tensorflow  :(
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

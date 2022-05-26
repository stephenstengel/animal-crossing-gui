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
import shutil
import tensorflow as tf
import time

from models import currentBestModel


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
	print("Testing! WOW!")
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
	images_ds = createDatasetFromImages(sourceStr)
	

	#It might be faster to load the model and weights separately. need testing.
	print("Loading model...")
	# ~ print("COMENTED OUT FOR TESTING!")
	theModel = tf.keras.models.load_model(CHECKPOINT_FOLDER )
	theModel.summary()
	
	#Get a list of predictions
	print("Making predictions...")
	startTime = time.time()
	predictionsArray = theModel.predict( \
			images_ds,
			verbose = 2, #shows a line? If we can print this to file, we can use it to inform our status bar.
			steps = 1, #only predict 1 batch of 32 pictures to test faster.
			)
	elapsedTime = time.time() - startTime
	print(str(predictionsArray))
	print("Prediction took: " + str(elapsedTime) + " seconds.")
	
	#For each prediction, put image into correct folder.
	# ~ sortPredictions(images_ds, predictionsArray, destStr, CLASS_NAMES_LIST_INT, CLASS_NAMES_LIST_STR)
	
	print("Done!")



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
	out_ds = tf.keras.preprocessing.image_dataset_from_directory( \
			sourceFolderStr,
			labels = None,
			label_mode = None,
			color_mode = "rgb",
			image_size = (IMG_HEIGHT, IMG_WIDTH), #triple check it is (h, w). Pillow files are (w, h) and need conversion to numpy/tensorflow by swapping height and width dimensions. (transpose?)
			batch_size = 32, #this might need tweaking depending on how much ram their computers have. 32 is default.
			shuffle = False,
			interpolation = "bilinear", #default is bilinear
			)
	return out_ds



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
	for folder in listDirsToDelete:
		if os.path.isdir(folder):
			shutil.rmtree(folder, ignore_errors = True)	






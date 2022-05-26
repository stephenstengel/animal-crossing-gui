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

from models import inceptionResNetModel


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


#should I use command line args? or save the requested folders to temp files?
#Actually, I can just import the functions from this file and call them directly!




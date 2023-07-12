"""  eeg-notebooks/eegnb/experiments/visual_n170/n170.py """

from psychopy import prefs
#change the pref libraty to PTB and set the latency mode to high precision
prefs.hardware['audioLib'] = 'PTB'
prefs.hardware['audioLatencyMode'] = 3

import os
from time import time
from glob import glob
from random import choice
from optparse import OptionParser
import random

import numpy as np
from pandas import DataFrame
from psychopy import visual, core, event

from eegnb.devices.eeg import EEG
from eegnb.stimuli import SUMMER_SCHOOL, FACE_HOUSE
#from eegnb.experiments import Experiment_modified as Experiment
from eegnb.summerschool import Experiment_modified as Experiment

SOA=2 # 0.3 image show time
ITI=1 # wait time between images
# mountains, faces, houses
images = ['houses', 'faces']

FOLDER1='faces'

FOLDER2='houses'

BACKGROUND_COLOR=[1,0.6,0.6]
JITTER=0.2
NTRIALS=2010
IMG_DISPLAY_SIZE=[20,20] #[10,10] #  width, height


class Summer_School_VisualN170(Experiment.BaseExperiment):

    def __init__(self, duration=120, eeg: EEG=None, save_fn=None,
            n_trials = NTRIALS, iti = ITI, soa = SOA, jitter = JITTER):

        # Set experiment name        
        exp_name = "Visual N170 modified"
        # Calling the super class constructor to initialize the experiment variables
        super(Summer_School_VisualN170, self).__init__(exp_name, duration, eeg, save_fn, n_trials, iti, soa, jitter, default_color=BACKGROUND_COLOR)

    def load_stimulus(self):
        
        # Loading Images from the folder
        load_image = lambda fn: visual.ImageStim(win=self.window, image=fn, size=IMG_DISPLAY_SIZE)

        # Setting up images for the stimulus
        #self.scene1 = list(map(load_image, glob(os.path.join(SUMMER_SCHOOL, FOLDER1, '*')))) # face
        #self.scene2 = list(map(load_image, glob(os.path.join(SUMMER_SCHOOL, FOLDER2, '*')))) # house
        self.imagelist = []
        for img in images:
            self.imagelist.append(list(map(load_image, glob(os.path.join(SUMMER_SCHOOL, img, '*')))))
        self.stimulus = images
        # Return the list of images as a stimulus object
        
        
    def present_stimulus(self, idx : int, trial):
        self.load_stimulus()

        # Get the image to be presented
        flk_sti = choice([x for x in range(len(self.imagelist))])
        image_choice = choice(self.imagelist[flk_sti])

        # Draw the image
        image_choice.draw()
        self.res_output_events[idx] = {
            'categories': self.stimulus[flk_sti],
        }
        self.res_output_dict = {
            'categories': {idx+1: self.stimulus[idx] for idx in range(len(self.stimulus))},
            'ITI': ITI,
            'SOA': SOA
        }
        # Pushing the sample to the EEG
        if self.eeg:
            timestamp = time()
            if self.eeg.backend == "muselsl":
                marker = [self.markernames[label]]
            else:
                marker = self.markernames[label]
            self.eeg.push_sample(marker=marker, timestamp=timestamp)
        
        self.window.flip()

        return []

if __name__ == "__main__":
    module = Summer_School_VisualN170()
    module.__init__()
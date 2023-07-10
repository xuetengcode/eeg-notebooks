
#from eegnb.experiments import Experiment
from eegnb.summerschool import Experiment_modified as Experiment
import os
from time import time
from glob import glob
import random

import numpy as np
from pandas import DataFrame
from psychopy import visual, core, event


from eegnb.devices.eeg import EEG
from eegnb import generate_save_fn
from eegnb.stimuli import SUMMER_SCHOOL, FACE_HOUSE

ITI=0.4
SOA=1
JITTER=0.2
NTRIALS=2010
STI_LOC_WIDTH=10
STI_LOC_HEIGHT=0

BACKGROUND_COLOR=[1,0.6,0.6]
FIXATION_COLOR=[1, 0, 0]
"""
[1,1,1] is white
[0,0,0] is grey
[-1,-1,-1] is black
[1.0,-1,-1] is red
[1.0,0.6,0.6] is pink
"""
images = ['houses', 'faces']
update_freq = [12, 15]
x_offset = [-10, 10]
y_offset = [0]

STI_CHOICE=1 # 0 for the original images, 1 for the pictures specified below
IMG_DISPLAY_SIZE=[10,10] #  width, height
T_ARROW=1 # 1 second
choice_of_second_img = 1
"""
    0: second image can be repetition of the first one
    1: second image exclude first one. images has to be >1
"""
Introduction_msg = """\nWelcome to the SSVEP experiment!\nStay still, focus on the stimuli, and try not to blink. \nThis block will run for %s seconds.\n
        Press spacebar to continue and c to terminate. \n"""

class Summer_School_Visual_Spatial_Attention(Experiment.BaseExperiment):

    def __init__(self, duration=120, eeg: EEG=None, save_fn=None, n_trials = NTRIALS, iti = ITI, soa = 0, jitter = JITTER):
        
        exp_name = "Visual Spatial Attention"
        self.image_size = IMG_DISPLAY_SIZE
        self.STI_LOC_WIDTH = 0
        self.STI_LOC_HEIGHT = 0

        self.multi_sti = choice_of_second_img 
        
        super().__init__(exp_name, duration, eeg, save_fn, n_trials, iti, soa, jitter, default_color=BACKGROUND_COLOR)

    def load_stimulus_img(self):

        # Loading Images from the folder
        load_image = lambda fn: visual.ImageStim(win=self.window, image=fn, size=IMG_DISPLAY_SIZE)

        # Setting up images for the stimulus
        self.imagelist = []
        for img in images:
            self.imagelist.append(list(map(load_image, glob(os.path.join(SUMMER_SCHOOL, img, '*')))))
        self.stimulus = images

    def load_stimulus(self):
        
        if STI_CHOICE == 0:
            #image_size = [40, 10]
            #self.image = visual.GratingStim(win=self.window, mask="circle", size=80, sf=0.2)
            self.image = visual.GratingStim(win=self.window, mask="sqr", size=self.image_size, sf=0.2, pos=(STI_LOC_WIDTH, STI_LOC_HEIGHT))
            
            #self.image_neg = visual.GratingStim(win=self.window, mask="circle", size=80, sf=0.2, phase=0.5)
            self.image_neg = visual.GratingStim(win=self.window, mask="sqr", size=self.image_size, sf=0.2, phase=0.5, pos=(STI_LOC_WIDTH, STI_LOC_HEIGHT))

            self.imagelist = [self.image, self.image_neg]
            self.stimulus = ['GratingStim']
        else:
            self.load_stimulus_img()

        fixation = visual.GratingStim(win=self.window, size=0.2, pos=[0, 0], sf=0.2, color=FIXATION_COLOR, autoDraw=True)

        self.arrow_left = visual.TextStim(win=self.window, text="""\n\u2190""", color=[-1, -1, -1])
        self.arrow_right = visual.TextStim(win=self.window, text="""\n\u2192""", color=[-1, -1, -1])

        # Generate the possible ssvep frequencies based on monitor refresh rate
        def get_possible_ssvep_freqs(frame_rate, stim_type="single"):
            
            max_period_nb = int(frame_rate / 6)
            periods = np.arange(max_period_nb) + 1
            
            if stim_type == "single":
                freqs = dict()
                for p1 in periods:
                    for p2 in periods:
                        f = frame_rate / (p1 + p2)
                        try:
                            freqs[f].append((p1, p2))
                        except:
                            freqs[f] = [(p1, p2)]

            elif stim_type == "reversal":
                freqs = {frame_rate / p: [(p, p)] for p in periods[::-1]}

            return freqs

        def init_flicker_stim(frame_rate, cycle, soa):
            
            if isinstance(cycle, tuple):
                stim_freq = frame_rate / sum(cycle)
                n_cycles = int(soa * stim_freq)
            
            else:
                stim_freq = frame_rate / cycle
                cycle = (cycle, cycle)
                n_cycles = int(soa * stim_freq) / 2
            
            return {"cycle": cycle, "freq": stim_freq, "n_cycles": n_cycles}

        # Set up stimuli, 7.5Hz (1:1), 12Hz (1:1)
        frame_rate = np.round(self.window.getActualFrameRate())  # Frame rate, in Hz
        self.frame_rate = frame_rate
        freqs = get_possible_ssvep_freqs(frame_rate, stim_type="reversal")
        self.stim_patterns = [
        init_flicker_stim(frame_rate, int(frame_rate/7.5), self.soa), # 2
        init_flicker_stim(frame_rate, int(frame_rate/12), self.soa), # 3
        ]
        
        print(
            (
                "Flickering frequencies (Hz): {}\n".format(
                    [self.stim_patterns[0]["freq"], self.stim_patterns[1]["freq"]]
                )
            )
        )

        return [
            init_flicker_stim(frame_rate, int(frame_rate/7.5), self.soa),
            init_flicker_stim(frame_rate, int(frame_rate/12), self.soa),
        ]


    def present_stimulus(self, idx, trial): # 2 flickr
        #self.window.color = BACKGROUND_COLOR
        
        # Select stimulus frequency
        ind = self.trials["parameter"].iloc[idx]
        
        # Push sample
        if self.eeg:
            timestamp = time()
            if self.eeg.backend == "muselsl":
                marker = [self.markernames[ind]]
            else:
                marker = self.markernames[ind]
            self.eeg.push_sample(marker=marker, timestamp=timestamp)
        
        # https://discourse.psychopy.org/t/i-need-advice-about-one-stimuli/29756/3
        # left \u2190 # right \u2192
        arr_choice = random.choice([0,1])
        if arr_choice == 0: # left
            stim_arrow = self.arrow_left
        else: # right
            stim_arrow = self.arrow_right

        # select the position of 7.5 Hz flickr
        # flk_pos = random.choice([0, 1]) # choose location
        flk_frq = random.choice([0, 1]) # choose frequency
        
        # Present flickering stim
        # https://stackoverflow.com/questions/37469796/where-can-i-find-flickering-functions-for-stimuli-on-psychopy-and-how-do-i-use
        
        # set flicker frequency
        flicker_frequency = update_freq[flk_frq]
        flicker_frequency_opposite = update_freq[flk_frq-1]
        
        sti_candidate = [x for x in range(len(self.imagelist))]
        if self.multi_sti == 0:
            flk_sti, flk_sti_opposite = random.choices(sti_candidate, k=2) # choose stimulus, allow any number of stimulus
        else:
            flk_sti, flk_sti_opposite = random.sample(sti_candidate, 2)
        # set image
        image_choice = random.choice(self.imagelist[flk_sti])
        image_choice_opposite = random.choice(self.imagelist[flk_sti_opposite])
        
        image_choice.pos = (x_offset[0], y_offset[0])
        image_choice_opposite.pos = (x_offset[1], y_offset[-1])
        
        # Push sample for marker
        #marker_content = 'flicker{}_freq{}_arrow{}'.format(flk_sti, flicker_frequency, arr_choice)
        marker_content = 1 # flk_frq + 1
        #print('idx: {}'.format(idx))

        # prepare json
        self.res_output[idx] = {
            'categories': [images[sti_candidate[flk_sti]], images[sti_candidate[flk_sti_opposite]]],
            'frequency': [flicker_frequency, flicker_frequency_opposite],
            'attention': [0, 1] if arr_choice == 0 else [1,0]
        }
        
        if self.eeg:
            timestamp = time()
            if self.eeg.backend == "muselsl":
                marker = [marker_content]
            else:
                marker = marker_content
            self.eeg.push_sample(marker=marker, timestamp=timestamp)

        image_choice.setAutoDraw(False)
        for _ in range(int(T_ARROW * self.frame_rate) ):
            stim_arrow.draw()
            self.window.flip()

        flicker_frame = self.frame_rate / (flicker_frequency * 2)
        flicker_frame_opposite = self.frame_rate / (flicker_frequency_opposite * 2)
        current_frame = 0
        for _ in range(int(SOA * self.frame_rate) ): #range(int(self.stim_patterns[ind]["cycle"][0])):
            if current_frame % (2*flicker_frame) < flicker_frame:
                image_choice.draw()
            if current_frame % (2*flicker_frame_opposite) < flicker_frame_opposite:
                image_choice_opposite.draw()
            
            self.window.flip()
            current_frame += 1  # increment by 1.
        
        self.random_record = [arr_choice, flk_sti]

        return self.random_record
    
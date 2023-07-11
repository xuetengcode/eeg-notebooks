# Welcome to the modified eeg-notebooks
### Git Repository
https://github.com/xuetengcode/eeg-notebooks
### Additional Images
https://drive.google.com/drive/folders/1AH47OELX5T4rQJRl1mi9CsPDGDnLMFIu?usp=sharing  
We have provided you with multiple images sets, in different folders. Below we explain each folder:  
**dogs, faces, houses, teapots**: pretty straightforward images of the different categories;  
**round_faces_houses**: faces and houses within a round aperture, so extent is approximately matched;  
**gratings**: blue and red gratings, tilted at different orientations, may be useful for something;  
**possible/impossible**: pictures of possible and impossible objects, created by Prof. Erez Freud (Freud, Ganel & Avidan, 2015);  
**blob_stimuli**: novel 3D objects, symmetrical and asymmetrical, rendered such that any symmetry either does ("ort") or does not ("per") show up on the retina. The four images within each set (e.g., "set001_") are matched for pairwise similarity (asym01 vs asym02, asym01 vs sym01, sym01 vs sym02) of low-level features within category ("ort" or "per"). Created by Prof. Kohler and used in ongoing work in the lab;  
**koh_images**: images from 10 different object categories (including "faces"), shown on unfamiliar backgrounds and viewpoints. 20 images per category, named in order (e.g., im0 - img19 are all bears). Used in ongoing work by Kohitij Kar and related to this a Journal of Neuroscience paper from a few years ago (Majaj et al., 2015);  
**cfmt_faces, cfmt_maskedfaces, cfmt_cars**: Pictures used in the Cambridge Face Memory Test (Duchaine & Nakayama, 2006). Single faces and triplets of faces. Later parts have added viewpoints and noise making the faces harder to recognize. "maskedfaces" are the same faces, but with masks. "cars" are from a car-based version of the same task (Dennett et al., 2012).

## Upon start
### On University computers
Open the terminal app and type:
```
cd eeg-notebook
git pull
```
The terminal should show either:
![System Diagram](git_pull1.jpeg)
or:
![System Diagram](git_pull2.jpeg)
If it shows an error message like this:
![System Diagram](git_error.jpeg)
Then reset the git by running:
```
git reset --hard
git pull
```
Now it shows something similar to the selected text (white background) and you can proceed to "Run the experiment":
![System Diagram](git_reset.jpeg)


### On your personal computer:

```
conda create -y -n eeg_experiments python=3.7 wxpython
conda activate eeg_experiments
```
clone the modified package and install:
```
git clone https://github.com/xuetengcode/eeg-notebooks.git
cd <to eeg-nootbooks folder>
pip install -e .
```

## Run the experiment
In the terminal, type:
```
eegnb runexp -ip
```
Then turn on your device:

Muse - short press once on the button to turn on. Press and hold to turn off.  
Unicorn - press and hold the power button until the light starts to blink, same way to turn off.

Now you select the device in the terminal:  
No device - `0`  
Muse 2 - `6`  
Muse s - `8`  
Unicorn - `13`

Then you select Experiments that start with "Summer_School", e.g., `6` for 6 - Summer_School_N170.

## Modify the experiment
Experiment codes are located at `~\eeg-notebooks\eegnb\summerschool\`
Go to summer_school_[experiment name], the file name of each experiment is: summer_school_[experiment name].py, e.g., `summer_school_visual_n170` --> `summer_school_n170.py`
![System Diagram](VisualExperiments.jpg)
In the experiment code, you can change the parameters to make your own experiment:

`SOA` - the duration of showing each image;  
`ITI` - the wait time between showings;  
`images` - stimulus categories. You can change or delete the image categories, e.g., `faces` --> `cats`. Image folders are located at `~\eeg-notebooks\eegnb\stimuli\visual\summer_school`, you can add new categories by adding new folders of images at this location;  
`NTRIALS` - leave it as 2010;  
`BACKGROUND_COLOR` - background color;  
`FIXATION_COLOR` - fixation (dot in the middle) color;  
`IMG_DISPLAY_SIZE` - image size on the screen;  
`T_ARROW` (when applicable) - presentation time of the arrow;  
`update_freq` (when applicable) - flickering frequency;  
`x_offset` (when applicable) - image location, horizontal distance away from center of screen;  
`y_offset` (when applicable) - image location, vertical distance away from center of screen.

## Collected Data

All data are saved at `~/.eegnb`. Click the top left corner `Activities` --> `Files` --> on the top tool bar, click the button with 3 short lines (Open Menu) --> select `Show Hidden Files`.  
Alternatively you can run the bash script `link_data.sh` in eeg-notebook folder:
```
bash link_data.sh
```
It will create a symbolic link from the hidden data folder to `~/eegnb`

## Visualize the data
Open a new terminal window:
```
cd ~\eeg-notebooks\eegnb\summerschool
jupyter notebook
```
Go to summer_school_[experiment name], then summer_school_[experiment name]_viz.ipnb. E.g., `summer_school_visual_n170` --> `summer_school_visual_n170_viz.ipnb`  
Replace the subject ID # and session #, then on the menu select `Cell` --> `Run All`

## More analyses to explore
* Source localization  
* Temporal evolution across electrodes  
* Other spectral estimation techniques either from libraries or even from scratch  
* Power band analysis  
* Integration in a simple BCI selection  
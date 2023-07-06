# Welcome to the modified eeg-notebooks
## Upon start
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


If you are on your personal computer:

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
Muse 2 - 6
Muse s - 8
Unicorn - 13

Then you select Experiments that start with "Summer_School", e.g., 6 - Summer_School_N170

## Modify the experiment
Experiment codes are located at ~\eeg-notebooks\eegnb\summerschool\
The file name of each experiment is: summer_school_[experiment name].py, e.g., 6 - summer_school_n170.py

The image folders are located at ~\eeg-notebooks\eegnb\stimuli\visual\summer_school
In the experiment code, you can change the image categories, e.g., "faces" --> "cats"

## Collected Data

All data are saved at `~/.eegnb`. Click the top left corner "Activities" --> "Files" --> on the top tool bar, click the button with 3 short lines (Open Menu) --> select "Show Hidden Files".
Alternatively you can run the bash script, `link_data.sh`, at eeg-notebook folder. It will create a symbolic link from the hidden data folderto `~/eegnb`

## Visualize the data
Open a new terminal window:
```
cd eeg-botebooks\eegnb\summerschool
jupyter notebook
```
Go to [experiment name], then [experiment name]_viz.ipnb. E.g., visual_n170 then visual_n170_viz.ipnb

Replace the subject ID # and session #, then on the menu select "Cell"- "Run All"

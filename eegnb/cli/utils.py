
#change the pref libraty to PTB and set the latency mode to high precision
from psychopy import prefs
prefs.hardware['audioLib'] = 'PTB'
prefs.hardware['audioLatencyMode'] = 3


from eegnb.devices.eeg import EEG

from eegnb.experiments import VisualN170
#from eegnb.experiments import VisualN170_modified
from eegnb.experiments import VisualP300
from eegnb.experiments import VisualSSVEP
from eegnb.experiments import AuditoryOddball
from eegnb.experiments.visual_cueing import cueing
from eegnb.experiments.visual_codeprose import codeprose
from eegnb.experiments.auditory_oddball import diaconescu
from eegnb.experiments.auditory_ssaep import ssaep, ssaep_onefreq

from eegnb.summerschool import Summer_School_VisualN170
from eegnb.summerschool import Summer_School_VisualP300
from eegnb.summerschool import Summer_School_VisualSSVEP
from eegnb.summerschool.visual_cueing import cueing as Summer_School_cueing
from eegnb.summerschool.visual_codeprose import codeprose as Summer_School_codeprose
#from eegnb.summerschool.auditory_oddball import diaconescu as Summer_School_diaconescu
from eegnb.summerschool.visual_gonogo import go_nogo as Summer_School_go_nogo

NEW_EXP = "Summer School"
# New Experiment Class structure has a different initilization, to be noted
experiments = {
    "visual-N170": VisualN170(),
    "visual-P300": VisualP300(),
    "visual-SSVEP": VisualSSVEP(),
    "visual-cue": cueing,
    "visual-codeprose": codeprose,
    #"auditory-SSAEP orig": ssaep,
    #"auditory-SSAEP onefreq": ssaep_onefreq,
    #"auditory-oddball orig": AuditoryOddball(),
    #"auditory-oddball diaconescu": diaconescu,
    "Summer School N170": Summer_School_VisualN170(),
    "Summer School P300": Summer_School_VisualP300(),
    "Summer School SSVEP": Summer_School_VisualSSVEP(),
    "Summer School visual-cue": Summer_School_cueing,
    "Summer School codeprose": Summer_School_codeprose,
    "Summer School GoNoGo": Summer_School_go_nogo,
}


def get_exp_desc(exp: str):
    if exp in experiments:
        module = experiments[exp]
        if hasattr(module, "__title__"):
            return module.__title__  # type: ignore
    return "{} (no description)".format(exp)


def run_experiment(
    experiment: str, eeg_device: EEG, record_duration: float = None, save_fn=None, my_img=None
):
    my_list = ["visual-N170", "visual-P300", "visual-SSVEP", "auditory-oddball orig",
            "Summer School N170", "Summer School P300","Summer School SSVEP"]
    if experiment in experiments:
        module = experiments[experiment]

        # Condition added for different run types of old and new experiment class structure
        if experiment in my_list:
            module.duration = record_duration
            module.eeg = eeg_device
            module.save_fn = save_fn
            module.run()
        else:
            module.present(duration=record_duration, eeg=eeg_device, save_fn=save_fn)  # type: ignore
    else:
        print("\nError: Unknown experiment '{}'".format(experiment))
        print("\nExperiment can be one of:")
        print("\n".join([" - " + exp for exp in experiments]))

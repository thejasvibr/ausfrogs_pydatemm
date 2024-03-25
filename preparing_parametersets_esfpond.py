'''
Localising overlapping calls: 2018-06-21
========================================
21st June 2018 is special as the microphone positions were exactly
measured using a TotalStation. Here let's try to localise sources in the audio file 
with POSIX timestamp 1529543496. This audio file corresponds to P00/8000 TMC of
the thermal cameras. 


Let's also create a new mic xyz set with <= 5cm positional error. 

'''
import glob
from natsort import natsorted
import matplotlib
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
#import pyvista as pv
import soundfile as sf
from scipy.spatial import distance_matrix, distance
euclidean = distance.euclidean
import os
import subprocess
import time
import tqdm
import yaml
np.random.seed(78464)

#%% first make a multichannel file from individual files
audiofiles = glob.glob('WSF_ESF_Pond/OLONG*.wav')
audio_data = [sf.read(each)[0] for each in audiofiles]
multich_data = np.array(audio_data).T
sf.write('olong_multichfile.wav', multich_data, sf.info(audiofiles[0]).samplerate)

#%% Then prepare a pseudo 3D mic xyz file
micxy = pd.read_csv('micxy.csv')
micxy['z'] = np.random.choice(np.linspace(0,0.05, 20), micxy.shape[0])
pseudo_3d_filename = 'pseudo_3d_ausfrog_micxyz.csv'
micxy.to_csv(pseudo_3d_filename)

#%% Now prepare the parameter file

common_parameters = {}
common_parameters['audiopath'] = 'olong_multichfile.wav'
common_parameters['arraygeompath'] = pseudo_3d_filename
common_parameters['dest_folder'] = 'ausfrogs_param_n_output'
common_parameters['K'] = 3
common_parameters['maxloopres'] = 1e-3
common_parameters['min_peak_dist'] = 0.5e-3 # s
common_parameters['thresh_tdoaresidual'] = 1e-8 # s
common_parameters['remove_lastchannel'] = "False"
common_parameters['run_name'] = 'ausfrogs'# the posix timestamp will be added later!

array_geom = pd.read_csv(common_parameters['arraygeompath']).loc[:,'x':'z'].to_numpy()

#%% Make the yaml file for the various time points
step_size = 0.05
window_size = 0.120
common_parameters['window_size'] = window_size
time_starts = np.arange(60, 90, step_size)

if not os.path.exists(common_parameters['dest_folder']):
    os.mkdir(common_parameters['dest_folder'])

# incoporate the time windows into the parameter file
relevant_time_windows = np.around(time_starts, 3)
# split the time_windows according to the total number of paramsets to be generated
split_timepoints = np.array_split(relevant_time_windows, 25)
#%%
for i, each in enumerate(split_timepoints):
    common_parameters['start_time'] = str(each.tolist())[1:-1]
    
    fname = os.path.join(common_parameters['dest_folder'], 
                         f'{common_parameters["run_name"]}_{i}.yaml')
    ff = open(fname, 'w+')
    yaml.dump(common_parameters, ff)




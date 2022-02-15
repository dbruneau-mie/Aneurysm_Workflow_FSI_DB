import matplotlib as mpl
mpl.use('Agg')
import os
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import postprocessing_common_h5py

"""
This script plots the compute time of the simulation graphically, from the logfiles generated on Scinet.

Args:
    case_path (Path): Path to results from simulation

"""

# Get input path
case_path = postprocessing_common_h5py.read_command_line()[0] 
case_name = os.path.basename(os.path.normpath(case_path)) # obtains only last folder in case_path
visualization_path = postprocessing_common_h5py.get_visualization_path(case_path)

# Get output path
imageFolder = os.path.join(visualization_path,'..',"Images")
if not os.path.exists(imageFolder):
    os.makedirs(imageFolder)


# find all logfiles in simulaation folder (file name must contain the word "logfile")
outLog=[file for file in os.listdir(case_path) if 'logfile' in file]

modified_lines=[]
time_sim=[]
compute_time_step=[]
n_outfiles = len(outLog)

print("Found {} output log files".format(n_outfiles))
if n_outfiles == 0:
    print("Found no output files - ensure the word 'logfile' is in the output text file name")

for idx in range(0,n_outfiles):
    # Open log file
    outLogPath=os.path.join(case_path,outLog[idx])
    file1 = open(outLogPath, 'r') 
    Lines = file1.readlines() 

    # Open log file get compute time and simulation time from that logfile 
    compute_time_total=0
    for line in Lines: 
        if 'Solved for timestep' in line:
            modified_lines.append(line)
            numb = re.findall("\d*\.?\d+", line) # take numbers from string
            time_sim.append(float(numb[1])) # This is the simulation time
            compute_time_step.append(float(numb[2])) # This is the compute time for that time step

# convert to numpy
time_sim=np.array(time_sim)
compute_time_step=np.array(compute_time_step)

# sort by increasing simulation time
ascending_t=np.argsort(time_sim, axis=0)
time_sim=time_sim[ascending_t]
compute_time_step=compute_time_step[ascending_t]

# Get cumulative compute time
compute_times = np.zeros(len(compute_time_step))
compute_time = 0
for idy in range(len(compute_time_step)):
    compute_time += compute_time_step[idy]
    compute_times[idy] = compute_time

compute_times = compute_times/60/60 # Convert to hours

# Plot and Save
plt.plot(time_sim,compute_times,label=case_name)
plt.title('Compute Time - ' + case_name)
plt.ylabel('Compute Time (Hrs)')
plt.xlabel('Simulation Time (s)')
plt.legend()
name=imageFolder+'/compute_time_'+case_name+'.png'
plt.savefig(name)  
plt.close()

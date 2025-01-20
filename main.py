# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:57:28 2024

@author: cbozonnet :(cyril.bozonnet@inrae.fr)
"""

import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from spectral import open_image
from processing_functions import mean_leaf_intensities  # Import your function

plt.close('all') # close all figures
plt.rc('text', usetex=True) # latex style
plt.rc('font', family='serif')

#  when running from R : Check if the 'skip_plots' flag is present in the arguments 
skip_plots = os.getenv("SKIP_PLOTS") == "TRUE"

############### Inputs ##############

lambda_min = 400 # [nm]
lambda_max = 1000 # [nm]

# Define list of files to process 
file_list = ['C:/Documents/traitement_image/Hyperspectral_Alex/code/test_image/hydrated/021.hdr',\
              'C:/Documents/traitement_image/Hyperspectral_Alex/code/test_image/dry/103.hdr']
#☻file_list = ['C:/Documents/traitement_image/Hyperspectral_Alex/code/test_image/hydrated/021.hdr']

# define list of reflectance files if it exists
reflect_file = None # never comment this line, comment just below to remove the optional file
#reflect_file = ['../Heat_wave/Control_coffee_well_hydrated/021/results/REFLECTANCE_021.hdr',\
#                '../Heat_wave/Dry_coffee_HW_drought/103/results/REFLECTANCE_103.hdr']

# define the legend
text_legend = {'Hydrated','Dried'}

############# Computations #########

# Loop through files and calculate mean leaf intensities
reflectance_list = []
for i, file in enumerate(file_list): 
    
    if reflect_file: # if the reflectance file is defined, use it
    
        reflect = reflect_file[i]
        
    else: # otherwise open data that allows computing it
    
        reflect=None
        
        # Extract directory and filename from filepath
        dir_path, file_name = os.path.split(file)
        base_name, _ = os.path.splitext(file_name)
    
        # Construct the complete paths to reference files
        whiteref_path = os.path.join(dir_path, f"WHITEREF_{base_name}.hdr")
        darkref_path = os.path.join(dir_path, f"DARKREF_{base_name}.hdr")
        
        # open whiteref data
        img = open_image(whiteref_path)
        data = img.load()
        whiteref_data = np.squeeze(data[0,0,:])
        
        # open darkref data
        img = open_image(darkref_path)
        data = img.load()
        darkref_data = np.squeeze(data[0,0,:])
        
    #call to the main function

    mean_intensities = mean_leaf_intensities(file,reflectance_file = reflect)  
    
    # store data
    if reflect_file: # if a reflection file is provided
        reflectance_list.append(mean_intensities) # mean leaf reflectance already obtained
    else: # otherwise compute it
        reflectance_list.append((mean_intensities-darkref_data)/(whiteref_data-darkref_data))
  


############# Plots ################
num_files = len(file_list)
n_band = reflectance_list[0].size
lambda_vec = np.linspace(lambda_min, lambda_max, n_band)
#Plot mean leaf intensities for all files (modify plot as needed)
if skip_plots==False:
    plt.figure()
    colors = plt.cm.viridis(np.linspace(0, 1, num_files))  # Generate colormap for lines
    for i, reflectance in enumerate(reflectance_list):
        plt.plot(lambda_vec,reflectance*100)    
    # add labels
    plt.legend(text_legend)
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Mean leaf reflectance [$\%$]')
    
    # Set grid and minor ticks
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.minorticks_on()
    
    # Use LaTeX for tick labels (optional)
    plt.tick_params(labelsize=12, which='both', top=True, bottom=True, left=True, right=True)
    #plt.tight_layout()
    
    plt.show()


# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:52:11 2024

@author: cbozonnet (cyril.bozonnet@inrae.fr)
"""

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from spectral import open_image
import matplotlib.patches as patches
from skimage.morphology import remove_small_objects, remove_small_holes
from skimage.measure import label, regionprops_table

def mean_leaf_intensities(file_path,reflectance_file=None): # create function
    """
    Processes a hyperspectral image, calculates mean intensities, and plots intermediate results.
    
    Args:
        file_path (str): Path to the hyperspectral image file (e.g., .hdr)
        reflectance_file (str, optional): path to a reflectance file to process
    
    Returns:
        np.ndarray: Array of mean leaf intensities for each wavelength
        np.ndarray: Array of mean square intensities
    """
    # Check if the 'skip_plots' flag is present in the arguments (when running from R)
    skip_plots = os.getenv("SKIP_PLOTS") == "TRUE"
    
    # get file name and path 
    dir_path, file_name = os.path.split(file_path)
    
    # Load the image
    img = open_image(file_path)
    data = img.load()
    
    # Select band of interest (modify as needed)
    band_view = data[:, :, 124] # to segment the leaves
    band_spots = data[:, :, 25] # to segment the bright spots
    
    # Threshold for bright spots
    thresh_spots = 800
    mask_spots = band_spots < thresh_spots
    
    # Find connected components in the mask
    labels_spots = label(~mask_spots)

    # Define area of interest coordinates (adjust as needed)
    x1, y1, x2, y2 = 160, 140, 400, 400
    
    # Create rectangle patch
    rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1, edgecolor='red', facecolor='none')
    
    # Zone mask
    mask_zone = np.zeros_like(band_view)
    mask_zone[y1:x2, x1:y2] = 1
    
    # Combine masks
    combined_mask = np.logical_and(mask_spots, mask_zone)
    
    # Threshold for leaves
    thresh_leaves = 350
    mask_leaves = band_view > thresh_leaves
    
    # Combine all masks
    combined_mask = np.logical_and(combined_mask, mask_leaves)
    
    # Label and clean mask
    my_label = label(combined_mask)
    cleared_label = remove_small_objects(my_label, min_size=120)
    cleared_mask = cleared_label > 0
    cleared_mask = remove_small_holes(cleared_mask, area_threshold=5)
    
    # Apply combined mask and calculate masked area
    masked_image = band_view * cleared_mask
    masked_area = np.sum(cleared_mask)
    
    # Calculate mean leaf intensities (MLI)
    if reflectance_file:
        other_img = open_image(reflectance_file)
        other_data = other_img.load()
        other_masked_data = other_data * cleared_mask
        MLI = np.sum(other_masked_data, axis=(0, 1)) * 1 / masked_area
    else: 
        MLI = np.sum(data * cleared_mask, axis=(0, 1)) * 1 / masked_area

    ############### create the plots #################

    if skip_plots==False:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))  # Create two subplots side-by-side

        # Plot band of interest in first subplot
        ax1.imshow(band_view, cmap='viridis')
        # Add colorbars using plt.colorbar
        plt.colorbar(ax1.imshow(band_view, cmap='viridis'))
        #ax1.colorbar()
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_title('View of the image + area selection')
        
        # Add the rectangle patch to the first subplot
        ax1.add_patch(rect)
        
        # Plot final image in second subplot
        if reflectance_file:
            ax2.imshow(other_masked_data[:,:,124],cmap='gray')
            plt.colorbar(ax2.imshow(other_masked_data[:,:,124], cmap='gray'))
        else:
            ax2.imshow(masked_image, cmap='gray')
            plt.colorbar(ax2.imshow(masked_image, cmap='gray'))
        #ax2.colorbar()
        ax2.set_title('Final image')
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        
        # Adjust layout (optional)
        plt.tight_layout()
        
        plt.show()
    
    # # # Mask for bright areas
    # # plt.figure()
    # # plt.imshow(square, cmap='gray')
    # # plt.colorbar()
    # # plt.title('Mask for bright spots')
    # # plt.show()

    return MLI

## Dependancies
You need to have the spectral library installed (pip install spectral)

## list of contents and description

open_hyper_plot.py : opens a hyperspectral image (or a 3D image) and display it along with a slider to move across the 3D stack.

processing_functions.py : image processing : remove bright spots, focus in a prescribed zone (a square zone that is amnually prescribed line 48), segment the leaves and clean the resulting binary mask (morphological operators), then apply the mask to the whole hyperspectral stack to compute the mean leaf intensity per wavelength. 

Segmentation is based on simple thresholding. Thresholds are manually prescribed (for other conditions they might not work! one could try an automatic threshold using Otsu for example). The wavelength on which to segment the leaves or the bright spots were manually chosen. This program also plots the original and segmented images to verify the segmentation.

main.py : launch the previous code for a list of files, compute the reflectance data, draw the plots

test_lauchPy_fromR.R : a R program to lauch the previous python program from R, get the data and plot them.



# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:45:02 2024

@author: cbozonnet
"""

# this code opens a hyperspectral image
# display it along with an interactive slider 
# to explore the image


import numpy as np
import matplotlib.pyplot as plt
from spectral import open_image
from matplotlib.widgets import Slider

plt.close('all') 
plt.rc('text', usetex=True) # latex style
plt.rc('font', family='serif')

# specify the file
path = '../Heat_wave/Control_coffee_well_hydrated/021/Capture/'
file = '021.hdr'
# path = '../Heat_wave/Control_coffee_well_hydrated/021/results/'
# file = 'REFLECTANCE_021.hdr'
# file = 'WHITEREF_021.hdr'
# path = '../Heat_wave/Dry_coffee_HW_drought/103/Capture/'
# file = '103.hdr'
full_path = path + file

# Charger l'image hyperspectrale
img = open_image(full_path)
data = img.load()

# Récupérer les dimensions de l'image et le nombre de longueurs d'onde
nx, ny, nb_longueurs_onde = data.shape

# Créer la figure et les axes
fig = plt.figure()
ax = fig.add_subplot(111)

# Fonction pour mettre à jour l'image affichée en fonction de la longueur d'onde
def update(val):
    # Récupérer l'indice de la longueur d'onde sélectionnée
    index = int(slider.val)
    
    # Afficher l'image correspondant à cette longueur d'onde
    ax.imshow(data[:, :, index], cmap='viridis')
    fig.canvas.draw_idle()

# Créer un slider pour sélectionner la longueur d'onde
axcolor = 'lightgoldenrodyellow'
axslider = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
slider = Slider(axslider, 'Longueur donde', 0, nb_longueurs_onde-1, valinit=0, valstep=1)
slider.on_changed(update)

# Afficher l'image initiale
ax.imshow(data[:, :, 0], cmap='viridis')
plt.subplots_adjust(bottom=0.2)
plt.show()
    

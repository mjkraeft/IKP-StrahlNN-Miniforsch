# -*- coding: utf-8 -*-
"""
Created on Wed May 17 11:03:01 2023
3D
@author: mseeger
"""

import numpy as np
import matplotlib.pyplot as plt

from mayavi import mlab
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D  #nur zur Erkennung


messungen=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22']
hoehe = np.arange(20,-21,-2)
breite = [7,11,13,15,15,17,17,19,19,19,21,19,19,19,17,17,15,15,13,11,7]

Bx_3d = np.zeros((21,21,66))
By_3d = np.zeros((21,21,66))
Bz_3d = np.zeros((21,21,66))
Babs_3d = np.zeros((21,21,66))

for n in range(21):
    data = np.loadtxt('Solenoid_Messung{}_3-5A_h{}.txt'.format(messungen[n],hoehe[n]),skiprows=6)
    xstart = int((21-breite[n])/2)
    xend = int(21 - xstart)
    Bx = np.reshape(data[:,4],(66,breite[n]))
    Bx[1::2, :] = Bx[1::2, ::-1]        
    By = np.reshape(data[:,5],(66,breite[n]))
    By[1::2, :] = By[1::2, ::-1]  
    Bz = np.reshape(data[:,6],(66,breite[n]))
    Bz[1::2, :] = Bz[1::2, ::-1]  
    Babs = np.reshape(data[:,3],(66,breite[n]))
    Babs[1::2, :] = Babs[1::2, ::-1] 
    Bx_3d[xstart:xend,20-n,:] = -By.transpose() #Umbauen in Strahlkoordinatensystem/Plotsystem
    By_3d[xstart:xend,20-n,:] = -Bx.transpose() #kein Minus! Minus von z-Richtungsumrechnung mal Minus von Magnetfeldumrechnung gibt plus!
    Bz_3d[xstart:xend,20-n,:] = -Bz.transpose()
    Babs_3d[xstart:xend,20-n,:] = Babs.transpose()
    
    
    
x, y, z = np.meshgrid(np.arange(22),
                      np.arange(22),
                      np.arange(67))
obj = mlab.quiver3d(Bx_3d,By_3d,Bz_3d, mode = 'arrow', colormap = 'viridis', vmin = 0, vmax = 0.035)
cb = mlab.colorbar(title='|B| in T',orientation='vertical', nb_labels=10)
cb.scalar_bar.unconstrained_font_size = True
cb.label_text_property.font_size=50
cb.title_text_property.font_size=50

mlab.show()
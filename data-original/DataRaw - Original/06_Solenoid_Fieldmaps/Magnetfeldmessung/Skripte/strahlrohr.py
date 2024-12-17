# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:57:31 2023

@author: Merle
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator,AutoMinorLocator)


#Lade Daten - Aus ohne - da müssen Seiten abgeschnitten werden!
aus_ohne = np.loadtxt('Solenoid_Messung32_0A_h0.txt',skiprows=6)
#Umformen Daten in Matrix
babs = np.reshape(aus_ohne[:,3],(66,21)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(aus_ohne[:,4],(66,21))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(aus_ohne[:,5],(66,21))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(aus_ohne[:,6],(66,21))
bz[1::2, :] = bz[1::2, ::-1]
#Umrechnen in Strahlkoordinatensystem
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_aus_ohne = -1000*by 
by_aus_ohne = 1000*bx
bz_aus_ohne = -1000*bz
babs_aus_ohne = 1000*babs

bx_aus_ohne = np.delete(bx_aus_ohne,[0,1,2,3,17,18,19,20],1)
by_aus_ohne = np.delete(by_aus_ohne,[0,1,2,3,17,18,19,20],1)
bz_aus_ohne = np.delete(bz_aus_ohne,[0,1,2,3,17,18,19,20],1)
babs_aus_ohne = np.delete(babs_aus_ohne,[0,1,2,3,17,18,19,20],1)

aus_mit = np.loadtxt('Solenoid_Messung49_0A_mitStrahlrohr_h0.txt',skiprows=6)
#Umformen Daten in Matrix
babs = np.reshape(aus_mit[:,3],(66,13)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(aus_mit[:,4],(66,13))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(aus_mit[:,5],(66,13))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(aus_mit[:,6],(66,13))
bz[1::2, :] = bz[1::2, ::-1]
#Umrechnen in Strahlkoordinatensystem
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_aus_mit = -1000*by 
by_aus_mit = 1000*bx
bz_aus_mit = -1000*bz
babs_aus_mit = 1000*babs

an_ohne = np.loadtxt('Solenoid_Messung51_3-5A_ohneStrahlrohr_h0.txt',skiprows=6)
#Umformen Daten in Matrix
babs = np.reshape(an_ohne[:,3],(66,13)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(an_ohne[:,4],(66,13))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(an_ohne[:,5],(66,13))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(an_ohne[:,6],(66,13))
bz[1::2, :] = bz[1::2, ::-1]
#Umrechnen in Strahlkoordinatensystem
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_an_ohne = -1000*by 
by_an_ohne = 1000*bx
bz_an_ohne = -1000*bz
babs_an_ohne = 1000*babs

an_mit = np.loadtxt('Solenoid_Messung50_3-5A_mitStrahlrohr_h0.txt',skiprows=6)
#Umformen Daten in Matrix
babs = np.reshape(an_mit[:,3],(66,13)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(an_mit[:,4],(66,13))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(an_mit[:,5],(66,13))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(an_mit[:,6],(66,13))
bz[1::2, :] = bz[1::2, ::-1]
#Umrechnen in Strahlkoordinatensystem
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_an_mit = -1000*by 
by_an_mit = 1000*bx
bz_an_mit = -1000*bz
babs_an_mit = 1000*babs

#2D-Plot Heatmap
plt.rc('xtick', labelsize=8)    # fontsize of the tick labels
plt.rc('ytick', labelsize=8)    # fontsize of the tick labels
plt.rc('axes', titlesize=10)     # fontsize of the axes title
plt.rc('axes', labelsize=10)    # fontsize of the x and y labels


xachse = np.arange(-1.0,1.1,1)  #Ticklabels x-Richtung
xstriche = np.arange(1,13,5)    #Tickpositionen x-Richtung

#Absolutes Feld
#3 Plots einer Ebene in einem: ohne Strahlrohr, mit Strahlrohr und die Differenz dazwischen
#imshow hat Ursprung in oberer linker Ecke, x-Achse geht nach unten, y-Achse nach rechts!
fig, (ax1,ax2,ax3) = plt.subplots(nrows=1,ncols=3,figsize = (9,5))#für 0A

im1 = ax1.imshow(babs_aus_ohne, cmap='viridis',vmin=0,vmax=0.11)
ax1.set_title('Without beam pipe')
ax1.set_xticks(xstriche)
ax1.set_xticklabels(xachse)
ax1.set_yticks(np.arange(0,66,5))
ax1.set_yticklabels(np.arange(-6.5,6.6,1))
ax1.xaxis.set_minor_locator(MultipleLocator(1))
ax1.set_xlabel('Position x in cm')
ax1.set_ylabel('Position z in cm')

im2 = ax2.imshow(babs_aus_mit, cmap='viridis',vmin=0,vmax=0.11)
ax2.set_xticks(xstriche)
ax2.set_xticklabels(xachse)
ax2.set_yticks(np.arange(0,66,5))
ax2.set_yticklabels(np.arange(-6.5,6.6,1))
ax2.set_title('With beam pipe')
ax2.xaxis.set_minor_locator(MultipleLocator(1))
ax2.set_xlabel('Position x in cm')
ax2.set_ylabel('Position z in cm')
cbar = ax2.figure.colorbar(im2, ax=ax2)
cbar.set_label('Magnetic field B in mT')

im3 = ax3.imshow(babs_aus_ohne-babs_aus_mit, cmap='RdBu',vmin=-0.004,vmax=0.004)
ax2.set_xticks(xstriche)
ax2.set_xticklabels(xachse)
ax3.set_yticks(np.arange(0,66,5))
ax3.set_yticklabels(np.arange(-6.5,6.6,1))
ax3.set_title('Difference')
ax3.xaxis.set_minor_locator(MultipleLocator(1))
ax3.set_xlabel('Position x in cm')
ax3.set_ylabel('Position z in cm')
cbar = ax3.figure.colorbar(im3, ax=ax3)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Effect of beam pipe on absolute magnetic field at 0 A',fontsize=12)
plt.savefig('Strahlrohr/xz_abs_0A.pdf',bbox_inches='tight')


fig, (ax3,ax4,ax5) = plt.subplots(nrows=1,ncols=3,figsize = (9,5))#für 3.5A

im3 = ax3.imshow(babs_an_ohne, cmap='viridis',vmin=0,vmax=35)
ax3.set_xticks(xstriche)
ax3.set_xticklabels(xachse)
ax3.set_yticks(np.arange(0,66,5))
ax3.set_yticklabels(np.arange(-6.5,6.6,1))
ax3.set_title('Without beam pipe')
ax3.xaxis.set_minor_locator(MultipleLocator(1))
ax3.set_xlabel('Position x in cm')
ax3.set_ylabel('Position z in cm')

im4 = ax4.imshow(babs_an_mit, cmap='viridis',vmin=0,vmax=35)
ax4.set_xticks(xstriche)
ax4.set_xticklabels(xachse)
ax4.set_yticks(np.arange(0,66,5))
ax4.set_yticklabels(np.arange(-6.5,6.6,1))
ax4.set_title('With beam pipe')
ax4.xaxis.set_minor_locator(MultipleLocator(1))   
ax4.set_xlabel('Position x in cm')
ax4.set_ylabel('Position z in cm')
cbar = ax4.figure.colorbar(im4, ax=ax4)
cbar.set_label('Magnetic field B in mT')

im5 = ax5.imshow(babs_an_mit-babs_an_ohne, cmap='RdBu',vmin=-0.04,vmax=0.04)
ax5.set_xticks(xstriche)
ax5.set_xticklabels(xachse)
ax5.set_yticks(np.arange(0,66,5))
ax5.set_yticklabels(np.arange(-6.5,6.6,1))
ax5.set_title('Difference')
ax5.xaxis.set_minor_locator(MultipleLocator(1))
ax5.set_xlabel('Position x in cm')
ax5.set_ylabel('Position z in cm')

cbar = ax5.figure.colorbar(im5, ax=ax5)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Effect of beam pipe on absolute magnetic field at 3.5 A',fontsize=12)
plt.savefig('Strahlrohr/xz_abs_3-5A.pdf',bbox_inches='tight')
plt.show()

#x-Feld
#3 Plots einer Ebene in einem: ohne Strahlrohr, mit Strahlrohr und die Differenz dazwischen
fig, (ax1,ax2,ax3) = plt.subplots(nrows=1,ncols=3,figsize = (9,5))#für 0A

im1 = ax1.imshow(bx_aus_ohne, cmap='viridis',vmin=-0.04,vmax=0.04)
ax1.set_title('Without beam pipe')
ax1.set_xticks(xstriche)
ax1.set_xticklabels(xachse)
ax1.set_yticks(np.arange(0,66,5))
ax1.set_yticklabels(np.arange(-6.5,6.6,1))
ax1.xaxis.set_minor_locator(MultipleLocator(1))
ax1.set_xlabel('Position x in cm')
ax1.set_ylabel('Position z in cm')
    
im2 = ax2.imshow(bx_aus_mit, cmap='viridis',vmin=-0.04,vmax=0.04)
ax2.set_xticks(xstriche)
ax2.set_xticklabels(xachse)
ax2.set_yticks(np.arange(0,66,5))
ax2.set_yticklabels(np.arange(-6.5,6.6,1))
ax2.set_title('With beam pipe')
ax2.xaxis.set_minor_locator(MultipleLocator(1))
ax2.set_xlabel('Position x in cm')
ax2.set_ylabel('Position z in cm')
cbar = ax2.figure.colorbar(im2, ax=ax2)
cbar.set_label('Magnetic field B in mT')

im3 = ax3.imshow(bx_aus_ohne-bx_aus_mit, cmap='RdBu',vmin=-0.005,vmax=0.005)
ax3.set_xticks(xstriche)
ax3.set_xticklabels(xachse)
ax3.set_yticks(np.arange(0,66,5))
ax3.set_yticklabels(np.arange(-6.5,6.6,1))
ax3.set_title('Difference')
ax3.xaxis.set_minor_locator(MultipleLocator(1))
ax3.set_xlabel('Position x in cm')
ax3.set_ylabel('Position z in cm')
cbar = ax3.figure.colorbar(im3, ax=ax3)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Effect of beam pipe on x-component of magn. field at 0A',fontsize=12)
plt.savefig('Strahlrohr/xz_x_0A.pdf',bbox_inches='tight')


fig, (ax3,ax4,ax5) = plt.subplots(nrows=1,ncols=3,figsize = (9,5))#für 3.5A

im3 = ax3.imshow(bx_an_ohne, cmap='viridis',vmin=-7,vmax=7)
ax3.set_xticks(xstriche)
ax3.set_xticklabels(xachse)
ax3.set_yticks(np.arange(0,66,5))
ax3.set_yticklabels(np.arange(-6.5,6.6,1))
ax3.set_title('Without beam pipe')
ax3.xaxis.set_minor_locator(MultipleLocator(1))
ax3.set_xlabel('Position x in cm')
ax3.set_ylabel('Position z in cm')

im4 = ax4.imshow(bx_an_mit, cmap='viridis',vmin=-7,vmax=7)
ax4.set_xticks(xstriche)
ax4.set_xticklabels(xachse)
ax4.set_yticks(np.arange(0,66,5))
ax4.set_yticklabels(np.arange(-6.5,6.6,1))
ax4.set_title('With beam pipe')
ax4.xaxis.set_minor_locator(MultipleLocator(1))   
ax4.set_xlabel('Position x in cm')
ax4.set_ylabel('Position z in cm')
cbar = ax4.figure.colorbar(im4, ax=ax4)
cbar.set_label('Magnetic field B in mT')

im5 = ax5.imshow(bx_an_mit-bx_an_ohne, cmap='RdBu',vmin=-0.03,vmax=0.03)
ax5.set_xticks(xstriche)
ax5.set_xticklabels(xachse)
ax5.set_yticks(np.arange(0,66,5))
ax5.set_yticklabels(np.arange(-6.5,6.6,1))
ax5.set_title('Difference')
ax5.xaxis.set_minor_locator(MultipleLocator(1))
ax5.set_xlabel('Position x in cm')
ax5.set_ylabel('Position z in cm')

cbar = ax5.figure.colorbar(im5, ax=ax5)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Effect of beam pipe on x-component of magn. field at 3.5 A',fontsize=12)
plt.savefig('Strahlrohr/xz_x_3.5A.pdf',bbox_inches='tight')
plt.show()

#y-Feld
#3 Plots einer Ebene in einem: ohne Strahlrohr, mit Strahlrohr und die Differenz dazwischen
fig, (ax1,ax2,ax3) = plt.subplots(nrows=1,ncols=3,figsize = (9,5))

im1 = ax1.imshow(by_aus_ohne, cmap='viridis',vmin=0,vmax=0.04)
ax1.set_title('Without beam pipe')
ax1.set_xticks(xstriche)
ax1.set_xticklabels(xachse)
ax1.set_yticks(np.arange(0,66,5))
ax1.set_yticklabels(np.arange(-6.5,6.6,1))
ax1.xaxis.set_minor_locator(MultipleLocator(1))
ax1.set_xlabel('Position x in cm')
ax1.set_ylabel('Position z in cm')
    
im2 = ax2.imshow(by_aus_mit, cmap='viridis',vmin=0,vmax=0.04)
ax2.set_xticks(xstriche)
ax2.set_xticklabels(xachse)
ax2.set_yticks(np.arange(0,66,5))
ax2.set_yticklabels(np.arange(-6.5,6.6,1))
ax2.set_title('With beam pipe')
ax2.xaxis.set_minor_locator(MultipleLocator(1))
ax2.set_xlabel('Position x in cm')
ax2.set_ylabel('Position z in cm')
cbar = ax2.figure.colorbar(im2, ax=ax2)
cbar.set_label('Magnetic field B in mT')

im3 = ax3.imshow(by_aus_ohne-by_aus_mit, cmap='RdBu',vmin=-0.006,vmax=0.006)
ax3.set_xticks(xstriche)
ax3.set_xticklabels(xachse)
ax3.set_yticks(np.arange(0,66,5))
ax3.set_yticklabels(np.arange(-6.5,6.6,1))
ax3.set_title('Difference')
ax3.xaxis.set_minor_locator(MultipleLocator(1))
ax3.set_xlabel('Position x in cm')
ax3.set_ylabel('Position z in cm')
cbar = ax3.figure.colorbar(im3, ax=ax3)
cbar.set_label('Magnetic field B in mT')

fig.suptitle('Effect of beam pipe on y-component of magn. field at 0 A',fontsize=12)
plt.savefig('Strahlrohr/xz_y_0A.pdf',bbox_inches='tight')


fig, (ax3,ax4,ax5) = plt.subplots(nrows=1,ncols=3,figsize = (9,5))

im3 = ax3.imshow(by_an_ohne, cmap='viridis',vmin=-0.05,vmax=0.35)
ax3.set_xticks(xstriche)
ax3.set_xticklabels(xachse)
ax3.set_yticks(np.arange(0,66,5))
ax3.set_yticklabels(np.arange(-6.5,6.6,1))
ax3.set_title('Without beam pipe')
ax3.xaxis.set_minor_locator(MultipleLocator(1))
ax3.set_xlabel('Position x in cm')
ax3.set_ylabel('Position z in cm')

im4 = ax4.imshow(by_an_mit, cmap='viridis',vmin=-0.05,vmax=0.35)
ax4.set_xticks(xstriche)
ax4.set_xticklabels(xachse)
ax4.set_yticks(np.arange(0,66,5))
ax4.set_yticklabels(np.arange(-6.5,6.6,1))
ax4.set_title('With beam pipe')
ax4.xaxis.set_minor_locator(MultipleLocator(1))   
ax4.set_xlabel('Position x in cm')
ax4.set_ylabel('Position z in cm')
cbar = ax4.figure.colorbar(im4, ax=ax4)
cbar.set_label('Magnetic field B in mT')

im5 = ax5.imshow(by_an_mit-by_an_ohne, cmap='RdBu',vmin=-0.004,vmax=0.004)
ax5.set_xticks(xstriche)
ax5.set_xticklabels(xachse)
ax5.set_yticks(np.arange(0,66,5))
ax5.set_yticklabels(np.arange(-6.5,6.6,1))
ax5.set_title('Difference')
ax5.xaxis.set_minor_locator(MultipleLocator(1))
ax5.set_xlabel('Position x in cm')
ax5.set_ylabel('Position z in cm')
cbar = ax5.figure.colorbar(im5, ax=ax5)
cbar.set_label('Magnetic field B in mT')

fig.suptitle('Effect of beam pipe on y-component of magn. field at 3.5 A',fontsize=12)
plt.savefig('Strahlrohr/xz_y_3-5A.pdf',bbox_inches='tight')
plt.show()

#z-Feld
#3 Plots einer Ebene in einem: ohne Strahlrohr, mit Strahlrohr und die Differenz dazwischen
fig, (ax1,ax2,ax3) = plt.subplots(nrows=1,ncols=3,figsize = (9,5))
im1 = ax1.imshow(bz_aus_ohne, cmap='viridis',vmin=0,vmax=0.11)
ax1.set_title('Without beam pipe')
ax1.set_xticks(xstriche)
ax1.set_xticklabels(xachse)
ax1.set_yticks(np.arange(0,66,5))
ax1.set_yticklabels(np.arange(-6.5,6.6,1))
ax1.xaxis.set_minor_locator(MultipleLocator(1))
ax1.set_xlabel('Position x in cm')
ax1.set_ylabel('Position z in cm')
    
im2 = ax2.imshow(bz_aus_mit, cmap='viridis',vmin=0,vmax=0.11)
ax2.set_xticks(xstriche)
ax2.set_xticklabels(xachse)
ax2.set_yticks(np.arange(0,66,5))
ax2.set_yticklabels(np.arange(-6.5,6.6,1))
ax2.set_title('With beam pipe')
ax2.xaxis.set_minor_locator(MultipleLocator(1))
ax2.set_xlabel('Position x in cm')
ax2.set_ylabel('Position z in cm')
cbar = ax2.figure.colorbar(im2, ax=ax2)
cbar.set_label('Magnetic field B in mT')

im3 = ax3.imshow(bz_aus_ohne-bz_aus_mit, cmap='RdBu',vmin=-0.004,vmax=0.004)
ax3.set_xticks(xstriche)
ax3.set_xticklabels(xachse)
ax3.set_yticks(np.arange(0,66,5))
ax3.set_yticklabels(np.arange(-6.5,6.6,1))
ax3.set_title('Difference')
ax3.xaxis.set_minor_locator(MultipleLocator(1))
ax3.set_xlabel('Position x in cm')
ax3.set_ylabel('Position z in cm')
cbar = ax3.figure.colorbar(im3, ax=ax3)
cbar.set_label('Magnetic field B in mT')

fig.suptitle('Effect of beam pipe on z-component of magn. field at 0 A',fontsize=12)
plt.savefig('Strahlrohr/xz_z_0A.pdf',bbox_inches='tight')

fig, (ax3,ax4,ax5) = plt.subplots(nrows=1,ncols=3,figsize = (9,5))

im3 = ax3.imshow(bz_an_ohne, cmap='viridis',vmin=0,vmax=35)
ax3.set_xticks(xstriche)
ax3.set_xticklabels(xachse)
ax3.set_yticks(np.arange(0,66,5))
ax3.set_yticklabels(np.arange(-6.5,6.6,1))
ax3.set_title('Without beam pipe')
ax3.xaxis.set_minor_locator(MultipleLocator(1))
ax3.set_xlabel('Position x in cm')
ax3.set_ylabel('Position z in cm')

im4 = ax4.imshow(bz_an_mit, cmap='viridis',vmin=0,vmax=35)
ax4.set_xticks(xstriche)
ax4.set_xticklabels(xachse)
ax4.set_yticks(np.arange(0,66,5))
ax4.set_yticklabels(np.arange(-6.5,6.6,1))
ax4.set_title('With beam pipe')
ax4.xaxis.set_minor_locator(MultipleLocator(1))   
ax4.set_xlabel('Position x in cm')
ax4.set_ylabel('Position z in cm')
cbar = ax4.figure.colorbar(im4, ax=ax4)

im5 = ax5.imshow(bz_an_mit-bz_an_ohne, cmap='RdBu',vmin=-0.04,vmax=0.04)
ax5.set_xticks(xstriche)
ax5.set_xticklabels(xachse)
ax5.set_yticks(np.arange(0,66,5))
ax5.set_yticklabels(np.arange(-6.5,6.6,1))
ax5.set_title('Difference')
ax5.xaxis.set_minor_locator(MultipleLocator(1))
ax5.set_xlabel('Position x in cm')
ax5.set_ylabel('Position z in cm')
cbar = ax5.figure.colorbar(im5, ax=ax5)
cbar.set_label('Magnetic field B in mT')

fig.suptitle('Effect of beam pipe on z-component of magn. field at 3.5 A',fontsize=12)
plt.savefig('Strahlrohr/xz_z_3-5A.pdf',bbox_inches='tight')
plt.show()

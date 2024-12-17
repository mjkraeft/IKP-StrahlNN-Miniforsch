# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 09:48:12 2023

@author: Merle
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as matplotlib

#Höhe 10
aus = np.full((66,44),np.nan)
aus_x = np.full((66,44),np.nan)
aus_y = np.full((66,44),np.nan)
aus_z = np.full((66,44),np.nan)

aus_seite = np.loadtxt('Solenoid_Messung43_0A_seite_h10.txt',skiprows=6)
#Umformen Daten in Matrix
babs = np.reshape(aus_seite[:,3],(66,11)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(aus_seite[:,4],(66,11))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(aus_seite[:,5],(66,11))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(aus_seite[:,6],(66,11))
bz[1::2, :] = bz[1::2, ::-1] 
    
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_real = -1000*by 
by_real = 1000*bx
bz_real = -1000*bz
babs = 1000*babs

aus[:,33:44] = babs
aus_x[:,33:44] = bx_real
aus_y[:,33:44] = by_real
aus_z[:,33:44] = bz_real

aus_vorne = np.loadtxt('Solenoid_Messung48_0A_vorne_h10.txt',skiprows=6)
#Umformen in Matrix
babs = np.reshape(aus_vorne[:,3],(11,33)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(aus_vorne[:,4],(11,33))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(aus_vorne[:,5],(11,33))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(aus_vorne[:,6],(11,33))
bz[1::2, :] = bz[1::2, ::-1] 
    
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_real = -1000*by 
by_real = 1000*bx
bz_real = -1000*bz
babs = 1000*babs

aus[:11,:33] = babs
aus_x[:11,:33] = bx_real
aus_y[:11,:33] = by_real
aus_z[:11,:33] = bz_real

#Mit Magnet an
an = np.full((66,44),np.nan)
an_x = np.full((66,44),np.nan)
an_y = np.full((66,44),np.nan)
an_z = np.full((66,44),np.nan)

an_seite = np.loadtxt('Solenoid_Messung52_3-5A_seite_h10.txt',skiprows=6)
#Umformen Daten in Matrix
babs = np.reshape(an_seite[:,3],(66,11)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(an_seite[:,4],(66,11))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(an_seite[:,5],(66,11))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(an_seite[:,6],(66,11))
bz[1::2, :] = bz[1::2, ::-1] 
    
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_real = -1000*by 
by_real = 1000*bx
bz_real = -1000*bz
babs = 1000*babs

an[:,33:44] = babs
an_x[:,33:44] = bx_real
an_y[:,33:44] = by_real
an_z[:,33:44] = bz_real

an_vorne = np.loadtxt('Solenoid_Messung57_3-5A_vorne_h10.txt',skiprows=6)
#Umformen in Matrix
babs = np.reshape(an_vorne[:,3],(11,33)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(an_vorne[:,4],(11,33))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(an_vorne[:,5],(11,33))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(an_vorne[:,6],(11,33))
bz[1::2, :] = bz[1::2, ::-1] 
    
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_real = -1000*by 
by_real = 1000*bx
bz_real = -1000*bz
babs = 1000*babs

an[:11,:33] = babs
an_x[:11,:33] = bx_real
an_y[:11,:33] = by_real
an_z[:11,:33] = bz_real

real = an - aus
real_x = an_x - aus_x
real_y = an_y - aus_y
real_z = an_z - aus_z
#Plotten
fig, ax = plt.subplots(figsize = (5,5))
current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='grey')
im = ax.imshow(real)
ax.set_xticks(np.arange(0,44,5))
ax.set_xticklabels(np.arange(0,8.8,1))
ax.set_yticks(np.arange(0,66,5))
ax.set_yticklabels(np.arange(-6.5,6.6,1))
    
ax.set_xlabel('Position x in cm')
ax.set_ylabel('Position z in cm')

cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Edge magnetic field in the x-z-plane',fontsize=10)
plt.savefig('Randfelder/randfeld_h10_abs.pdf')
plt.show()

#Plotten
fig, ax = plt.subplots(figsize = (5,5))
current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='grey')
im = ax.imshow(real_x)
ax.set_xticks(np.arange(0,44,5))
ax.set_xticklabels(np.arange(0,8.8,1))
ax.set_yticks(np.arange(0,66,5))
ax.set_yticklabels(np.arange(-6.5,6.6,1))
    
ax.set_xlabel('Position x in cm')
ax.set_ylabel('Position z in cm')

cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Magnetic field in the x-z-plane',fontsize=10)
plt.savefig('Randfelder/randfeld_h10_x.pdf')
plt.show()

#Plotten
fig, ax = plt.subplots(figsize = (5,5))
current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='grey')
im = ax.imshow(real_y)
ax.set_xticks(np.arange(0,44,5))
ax.set_xticklabels(np.arange(0,8.8,1))
ax.set_yticks(np.arange(0,66,5))
ax.set_yticklabels(np.arange(-6.5,6.6,1))
    
ax.set_xlabel('Position x in cm')
ax.set_ylabel('Position z in cm')

cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Magnetic field in the x-z-plane',fontsize=10)
plt.savefig('Randfelder/randfeld_h10_y.pdf')
plt.show()

#Plotten
fig, ax = plt.subplots(figsize = (5,5))
current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='grey')
im = ax.imshow(real_z)
ax.set_xticks(np.arange(0,44,5))
ax.set_xticklabels(np.arange(0,8.8,1))
ax.set_yticks(np.arange(0,66,5))
ax.set_yticklabels(np.arange(-6.5,6.6,1))
    
ax.set_xlabel('Position x in cm')
ax.set_ylabel('Position z in cm')

cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Magnetic field in the x-z-plane',fontsize=10)
plt.savefig('Randfelder/randfeld_h10_z.pdf')
plt.show()

#Höhe 0
aus = np.full((66,44),np.nan)
aus_x = np.full((66,44),np.nan)
aus_y = np.full((66,44),np.nan)
aus_z = np.full((66,44),np.nan)

aus_seite = np.loadtxt('Solenoid_Messung44_0A_seite_h0.txt',skiprows=6)
#Umformen Daten in Matrix
babs = np.reshape(aus_seite[:,3],(66,11)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(aus_seite[:,4],(66,11))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(aus_seite[:,5],(66,11))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(aus_seite[:,6],(66,11))
bz[1::2, :] = bz[1::2, ::-1] 
    
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_real = -1000*by 
by_real = 1000*bx
bz_real = -1000*bz
babs = 1000*babs

aus[:,33:44] = babs
aus_x[:,33:44] = bx_real
aus_y[:,33:44] = by_real
aus_z[:,33:44] = bz_real

aus_vorne = np.loadtxt('Solenoid_Messung47_0A_vorne_h0.txt',skiprows=6)
#Umformen in Matrix
babs = np.reshape(aus_vorne[:,3],(11,33)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(aus_vorne[:,4],(11,33))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(aus_vorne[:,5],(11,33))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(aus_vorne[:,6],(11,33))
bz[1::2, :] = bz[1::2, ::-1] 
    
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_real = -1000*by 
by_real = 1000*bx
bz_real = -1000*bz
babs = 1000*babs

aus[:11,:33] = babs
aus_x[:11,:33] = bx_real
aus_y[:11,:33] = by_real
aus_z[:11,:33] = bz_real

#Mit Magnet an
an = np.full((66,44),np.nan)
an_x = np.full((66,44),np.nan)
an_y = np.full((66,44),np.nan)
an_z = np.full((66,44),np.nan)

an_seite = np.loadtxt('Solenoid_Messung53_3-5A_seite_h0.txt',skiprows=6)
#Umformen Daten in Matrix
babs = np.reshape(an_seite[:,3],(66,11)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(an_seite[:,4],(66,11))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(an_seite[:,5],(66,11))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(an_seite[:,6],(66,11))
bz[1::2, :] = bz[1::2, ::-1] 
    
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_real = -1000*by 
by_real = 1000*bx
bz_real = -1000*bz
babs = 1000*babs

an[:,33:44] = babs
an_x[:,33:44] = bx_real
an_y[:,33:44] = by_real
an_z[:,33:44] = bz_real

an_vorne = np.loadtxt('Solenoid_Messung56_3-5A_vorne_h0.txt',skiprows=6)
#Umformen in Matrix
babs = np.reshape(an_vorne[:,3],(11,33)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(an_vorne[:,4],(11,33))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(an_vorne[:,5],(11,33))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(an_vorne[:,6],(11,33))
bz[1::2, :] = bz[1::2, ::-1] 
    
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_real = -1000*by 
by_real = 1000*bx
bz_real = -1000*bz
babs = 1000*babs

an[:11,:33] = babs
an_x[:11,:33] = bx_real
an_y[:11,:33] = by_real
an_z[:11,:33] = bz_real

real = an - aus
real_x = an_x - aus_x
real_y = an_y - aus_y
real_z = an_z - aus_z
#Plotten
fig, ax = plt.subplots(figsize = (5,5))
current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='grey')
im = ax.imshow(real)
ax.set_xticks(np.arange(0,44,5))
ax.set_xticklabels(np.arange(0,8.8,1))
ax.set_yticks(np.arange(0,66,5))
ax.set_yticklabels(np.arange(-6.5,6.6,1))
    
ax.set_xlabel('Position x in cm')
ax.set_ylabel('Position z in cm')

cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Edge magnetic field in the x-z-plane',fontsize=10)
plt.savefig('Randfelder/randfeld_h0_abs.pdf')
plt.show()

#Plotten
fig, ax = plt.subplots(figsize = (5,5))
current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='grey')
im = ax.imshow(real_x)
ax.set_xticks(np.arange(0,44,5))
ax.set_xticklabels(np.arange(0,8.8,1))
ax.set_yticks(np.arange(0,66,5))
ax.set_yticklabels(np.arange(-6.5,6.6,1))
    
ax.set_xlabel('Position x in cm')
ax.set_ylabel('Position z in cm')

cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Magnetic field in the x-z-plane',fontsize=10)
plt.savefig('Randfelder/randfeld_h0_x.pdf')
plt.show()

#Plotten
fig, ax = plt.subplots(figsize = (5,5))
current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='grey')
im = ax.imshow(real_y)
ax.set_xticks(np.arange(0,44,5))
ax.set_xticklabels(np.arange(0,8.8,1))
ax.set_yticks(np.arange(0,66,5))
ax.set_yticklabels(np.arange(-6.5,6.6,1))
    
ax.set_xlabel('Position x in cm')
ax.set_ylabel('Position z in cm')

cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Magnetic field in the x-z-plane',fontsize=10)
plt.savefig('Randfelder/randfeld_h0_y.pdf')
plt.show()

#Plotten
fig, ax = plt.subplots(figsize = (5,5))
current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='grey')
im = ax.imshow(real_z)
ax.set_xticks(np.arange(0,44,5))
ax.set_xticklabels(np.arange(0,8.8,1))
ax.set_yticks(np.arange(0,66,5))
ax.set_yticklabels(np.arange(-6.5,6.6,1))
    
ax.set_xlabel('Position x in cm')
ax.set_ylabel('Position z in cm')

cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Magnetic field in the x-z-plane',fontsize=10)
plt.savefig('Randfelder/randfeld_h0_z.pdf')
plt.show()

#Höhe -10
aus = np.full((66,44),np.nan)
aus_x = np.full((66,44),np.nan)
aus_y = np.full((66,44),np.nan)
aus_z = np.full((66,44),np.nan)

aus_seite = np.loadtxt('Solenoid_Messung45_0A_seite_h-10.txt',skiprows=6)
#Umformen Daten in Matrix
babs = np.reshape(aus_seite[:,3],(66,10)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(aus_seite[:,4],(66,10))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(aus_seite[:,5],(66,10))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(aus_seite[:,6],(66,10))
bz[1::2, :] = bz[1::2, ::-1] 
    
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_real = -1000*by 
by_real = 1000*bx
bz_real = -1000*bz
babs = 1000*babs

aus[:,34:44] = babs
aus_x[:,34:44] = bx_real
aus_y[:,34:44] = by_real
aus_z[:,34:44] = bz_real

aus_vorne = np.loadtxt('Solenoid_Messung46_0A_vorne_h-10.txt',skiprows=6)
#Umformen in Matrix
babs = np.reshape(aus_vorne[:,3],(11,34)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(aus_vorne[:,4],(11,34))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(aus_vorne[:,5],(11,34))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(aus_vorne[:,6],(11,34))
bz[1::2, :] = bz[1::2, ::-1] 
    
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_real = -1000*by 
by_real = 1000*bx
bz_real = -1000*bz
babs = 1000*babs

aus[:11,:34] = babs
aus_x[:11,:34] = bx_real
aus_y[:11,:34] = by_real
aus_z[:11,:34] = bz_real

#Mit Magnet an
an = np.full((66,44),np.nan)
an_x = np.full((66,44),np.nan)
an_y = np.full((66,44),np.nan)
an_z = np.full((66,44),np.nan)

an_seite = np.loadtxt('Solenoid_Messung54_3-5A_seite_h-10.txt',skiprows=6)
#Umformen Daten in Matrix
babs = np.reshape(an_seite[:,3],(66,10)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(an_seite[:,4],(66,10))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(an_seite[:,5],(66,10))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(an_seite[:,6],(66,10))
bz[1::2, :] = bz[1::2, ::-1] 
    
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_real = -1000*by 
by_real = 1000*bx
bz_real = -1000*bz
babs = 1000*babs

an[:,34:44] = babs
an_x[:,34:44] = bx_real
an_y[:,34:44] = by_real
an_z[:,34:44] = bz_real

an_vorne = np.loadtxt('Solenoid_Messung55_3-5A_vorne_h-10.txt',skiprows=6)
#Umformen in Matrix
babs = np.reshape(an_vorne[:,3],(11,34)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
bx = np.reshape(an_vorne[:,4],(11,34))
bx[1::2, :] = bx[1::2, ::-1]
by = np.reshape(an_vorne[:,5],(11,34))
by[1::2, :] = by[1::2, ::-1]
bz = np.reshape(an_vorne[:,6],(11,34))
bz[1::2, :] = bz[1::2, ::-1] 
    
#Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
bx_real = -1000*by 
by_real = 1000*bx
bz_real = -1000*bz
babs = 1000*babs

an[:11,:34] = babs
an_x[:11,:34] = bx_real
an_y[:11,:34] = by_real
an_z[:11,:34] = bz_real

real = an - aus
real_x = an_x - aus_x
real_y = an_y - aus_y
real_z = an_z - aus_z
#Plotten
fig, ax = plt.subplots(figsize = (5,5))
current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='grey')
im = ax.imshow(real)
ax.set_xticks(np.arange(0,44,5))
ax.set_xticklabels(np.arange(0,8.8,1))
ax.set_yticks(np.arange(0,66,5))
ax.set_yticklabels(np.arange(-6.5,6.6,1))
    
ax.set_xlabel('Position x in cm')
ax.set_ylabel('Position z in cm')

cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Edge magnetic field in the x-z-plane',fontsize=10)
plt.savefig('Randfelder/randfeld_h-10_abs.pdf')
plt.show()

#Plotten
fig, ax = plt.subplots(figsize = (5,5))
current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='grey')
im = ax.imshow(real_x)
ax.set_xticks(np.arange(0,44,5))
ax.set_xticklabels(np.arange(0,8.8,1))
ax.set_yticks(np.arange(0,66,5))
ax.set_yticklabels(np.arange(-6.5,6.6,1))
    
ax.set_xlabel('Position x in cm')
ax.set_ylabel('Position z in cm')

cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Magnetic field in the x-z-plane',fontsize=10)
plt.savefig('Randfelder/randfeld_h-10_x.pdf')
plt.show()

#Plotten
fig, ax = plt.subplots(figsize = (5,5))
current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='grey')
im = ax.imshow(real_y)
ax.set_xticks(np.arange(0,44,5))
ax.set_xticklabels(np.arange(0,8.8,1))
ax.set_yticks(np.arange(0,66,5))
ax.set_yticklabels(np.arange(-6.5,6.6,1))
    
ax.set_xlabel('Position x in cm')
ax.set_ylabel('Position z in cm')

cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Magnetic field in the x-z-plane',fontsize=10)
plt.savefig('Randfelder/randfeld_h-10_y.pdf')
plt.show()

#Plotten
fig, ax = plt.subplots(figsize = (5,5))
current_cmap = matplotlib.cm.get_cmap()
current_cmap.set_bad(color='grey')
im = ax.imshow(real_z)
ax.set_xticks(np.arange(0,44,5))
ax.set_xticklabels(np.arange(0,8.8,1))
ax.set_yticks(np.arange(0,66,5))
ax.set_yticklabels(np.arange(-6.5,6.6,1))
    
ax.set_xlabel('Position x in cm')
ax.set_ylabel('Position z in cm')

cbar = ax.figure.colorbar(im, ax=ax)
cbar.set_label('Magnetic field B in mT')
fig.suptitle('Magnetic field in the x-z-plane',fontsize=10)
plt.savefig('Randfelder/randfeld_h-10_z.pdf')
plt.show()
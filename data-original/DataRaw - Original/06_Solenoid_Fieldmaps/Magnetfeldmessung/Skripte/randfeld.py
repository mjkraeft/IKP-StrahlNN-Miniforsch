# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 08:29:39 2023
Auswertung Randfelder 

Format Dateien: 6 Infozeilen oben
Spalte 1-3: x,y,z Koordinate
Spalte 4: Babs
Spalte 5-8: Bx,By,Bz
@author: Merle
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator,AutoMinorLocator)

#Lade Daten
#Reihenfolge seite:oben,mitte,unten;vorne:oben,mitte,unten
aus = ['Solenoid_Messung43_0A_seite_h10.txt','Solenoid_Messung44_0A_seite_h0.txt',
       'Solenoid_Messung45_0A_seite_h-10.txt','Solenoid_Messung48_0A_vorne_h10.txt',
       'Solenoid_Messung47_0A_vorne_h0.txt','Solenoid_Messung46_0A_vorne_h-10.txt']
         
         
an = ['Solenoid_Messung52_3-5A_seite_h10.txt','Solenoid_Messung53_3-5A_seite_h0.txt',
      'Solenoid_Messung54_3-5A_seite_h-10.txt','Solenoid_Messung57_3-5A_vorne_h10.txt',
      'Solenoid_Messung56_3-5A_vorne_h0.txt','Solenoid_Messung55_3-5A_vorne_h-10.txt']

#Infos für die Schleife
breite = [11,11,10,33,33,34]
laenge = [66,66,66,11,11,11]
name = ['seite_oben','seite_mitte','seite_unten','vorne_oben','vorne_mitte','vorne_unten']
hoehe = [1,0,-1,1,0,-1]

for n in range(3):
    #Laden aller Daten
    ebene = np.loadtxt('{}'.format(an[n]),skiprows=6)
    ebene_ug = np.loadtxt('{}'.format(aus[n]),skiprows=6)
    
    #Umformen Daten in Matrix - Magnet an
    babs = np.reshape(ebene[:,3],(laenge[n],breite[n])) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
    babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
    bx = np.reshape(ebene[:,4],(laenge[n],breite[n]))
    bx[1::2, :] = bx[1::2, ::-1]
    by = np.reshape(ebene[:,5],(laenge[n],breite[n]))
    by[1::2, :] = by[1::2, ::-1]
    bz = np.reshape(ebene[:,6],(laenge[n],breite[n]))
    bz[1::2, :] = bz[1::2, ::-1] 
    
    #Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
    bx_real = -1000*by 
    by_real = 1000*bx
    bz_real = -1000*bz
    babs = 1000*babs
    
    #Umformen Daten in Matrix - Magnet aus (Untergrund)
    babs_ug = np.reshape(ebene_ug[:,3],(laenge[n],breite[n])) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
    babs_ug[1::2, :] = babs_ug[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
    bx_ug = np.reshape(ebene_ug[:,4],(laenge[n],breite[n]))
    bx_ug[1::2, :] = bx_ug[1::2, ::-1]
    by_ug = np.reshape(ebene_ug[:,5],(laenge[n],breite[n]))
    by_ug[1::2, :] = by_ug[1::2, ::-1]
    bz_ug = np.reshape(ebene_ug[:,6],(laenge[n],breite[n]))
    bz_ug[1::2, :] = bz_ug[1::2, ::-1] 
    
    #Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
    bx_real_ug = -1000*by_ug 
    by_real_ug = 1000*bx_ug
    bz_real_ug = -1000*bz_ug
    babs_ug = 1000*babs_ug
    
    #Bereinigtes Magnetfeld (Untergrund abgezogen)
    babs_bereinigt = babs - babs_ug
    bx_bereinigt = bx_real - bx_real_ug
    by_bereinigt = by_real - by_real_ug
    bz_bereinigt = bz_real - bz_real_ug
    

    #2D-Plot Heatmap
    xachse=np.arange(6.4,8.5,1)
    xstriche=np.arange(0,11,5)
    zachse = np.arange(-6.5,6.6,1)
    
    plt.rc('xtick', labelsize=8)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=8)    # fontsize of the tick labels
    
    #4 Plots einer Ebene in einem
    #imshow hat Ursprung in oberer linker Ecke, x-Achse geht nach unten, y-Achse nach rechts!
    fig, (ax1,ax2,ax3,ax4) = plt.subplots(nrows=1,ncols=4,figsize = (10,4.5))
    im1 = ax1.imshow(babs_bereinigt, cmap='viridis',vmin=0,vmax=0.08)
    ax1.set_title('Abs.')
    ax1.set_xticks(xstriche)
    ax1.set_xticklabels(xachse)
    ax1.set_yticks(np.arange(0,66,5))
    ax1.set_yticklabels(zachse)
    ax1.xaxis.set_minor_locator(MultipleLocator(1))
    cbar = ax1.figure.colorbar(im1, ax=ax1)
    
    ax1.set_xlabel('Position x in cm')
    ax1.set_ylabel('Position z in cm')
    
    #cbar = ax1.figure.colorbar(im4, ax=ax4)
    im2 = ax2.imshow(bx_bereinigt, cmap='viridis',vmin=-0.08,vmax=0.08)
    ax2.set_xticks(xstriche)
    ax2.set_xticklabels(xachse)
    ax2.set_yticks(np.arange(0,66,5))
    ax2.set_yticklabels(zachse)
    ax2.set_title('x')
    ax2.xaxis.set_minor_locator(MultipleLocator(1))
    
    cbar = ax2.figure.colorbar(im2, ax=ax2)
    ax2.set_xlabel('Position x in cm')
    ax2.set_ylabel('Position z in cm')
    
    #cbar = ax2.figure.colorbar(im4, ax=ax4)
    im3 = ax3.imshow(by_bereinigt, cmap='viridis',vmin=-0.015,vmax=0.015)
    ax3.set_xticks(xstriche)
    ax3.set_xticklabels(xachse)
    ax3.set_yticks(np.arange(0,66,5))
    ax3.set_yticklabels(zachse)
    ax3.set_title('y')
    ax3.xaxis.set_minor_locator(MultipleLocator(1))
    cbar = ax3.figure.colorbar(im3, ax=ax3)
    
    ax3.set_xlabel('Position x in cm')
    ax3.set_ylabel('Position z in cm')
    
    #cbar = ax3.figure.colorbar(im4, ax=ax4)
    im4 = ax4.imshow(bz_bereinigt, cmap='viridis',vmin=-0.1,vmax=0)
    ax4.set_xticks(xstriche)
    ax4.set_xticklabels(xachse)
    ax4.set_yticks(np.arange(0,66,5))
    ax4.set_yticklabels(zachse)
    ax4.set_title('z')
    ax4.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax4.set_xlabel('Position x in cm')
    ax4.set_ylabel('Position z in cm')
    cbar = ax4.figure.colorbar(im4, ax=ax4)
    cbar.set_label('Magnetic field B in mT')
    fig.suptitle('Edge magnetic field on the side of the magnet in the x-z-plane at height y={} cm'.format(hoehe[n]))
    plt.savefig('Randfelder/randfeld_ebene_{}.pdf'.format(name[n]),bbox_inches='tight')
    plt.show()

for n in range(3,6):
    #Laden aller Daten
    ebene = np.loadtxt('{}'.format(an[n]),skiprows=6)
    ebene_ug = np.loadtxt('{}'.format(aus[n]),skiprows=6)
    
    #Umformen Daten in Matrix - Magnet an
    babs = np.reshape(ebene[:,3],(laenge[n],breite[n])) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
    babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
    bx = np.reshape(ebene[:,4],(laenge[n],breite[n]))
    bx[1::2, :] = bx[1::2, ::-1]
    by = np.reshape(ebene[:,5],(laenge[n],breite[n]))
    by[1::2, :] = by[1::2, ::-1]
    bz = np.reshape(ebene[:,6],(laenge[n],breite[n]))
    bz[1::2, :] = bz[1::2, ::-1] 
    
    #Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
    bx_real = -1000*by 
    by_real = 1000*bx
    bz_real = -1000*bz
    babs = 1000*babs
    
    #Umformen Daten in Matrix - Magnet aus (Untergrund)
    babs_ug = np.reshape(ebene_ug[:,3],(laenge[n],breite[n])) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
    babs_ug[1::2, :] = babs_ug[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
    bx_ug = np.reshape(ebene_ug[:,4],(laenge[n],breite[n]))
    bx_ug[1::2, :] = bx_ug[1::2, ::-1]
    by_ug = np.reshape(ebene_ug[:,5],(laenge[n],breite[n]))
    by_ug[1::2, :] = by_ug[1::2, ::-1]
    bz_ug = np.reshape(ebene_ug[:,6],(laenge[n],breite[n]))
    bz_ug[1::2, :] = bz_ug[1::2, ::-1] 
    
    #Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
    bx_real_ug = -1000*by_ug 
    by_real_ug = 1000*bx_ug
    bz_real_ug = -1000*bz_ug
    babs_ug = 1000*babs_ug
    
    #Bereinigtes Magnetfeld (Untergrund abgezogen)
    babs_bereinigt = babs - babs_ug
    bx_bereinigt = bx_real - bx_real_ug
    by_bereinigt = by_real - by_real_ug
    bz_bereinigt = bz_real - bz_real_ug
    

    #2D-Plot Heatmap
    xstriche = np.arange(0,32,5)
    xachse = np.arange(0,6.4,1)
    zstriche = np.arange(0,11,5)
    zachse = np.arange(-6.5,-4.4,1)
    #4 Plots einer Ebene in einem
    #imshow hat Ursprung in oberer linker Ecke, x-Achse geht nach unten, y-Achse nach rechts!
    fig, ([ax1,ax2],[ax3,ax4]) = plt.subplots(nrows=2,ncols=2,figsize = (10,5))
    im1 = ax1.imshow(babs_bereinigt, cmap='viridis',vmin=-0.8,vmax=0.8)
    ax1.set_title('Abs.')
    ax1.set_xticks(xstriche)
    ax1.set_xticklabels(xachse)
    ax1.set_yticks(zstriche)
    ax1.set_yticklabels(zachse)
    ax1.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax1.set_xlabel('Position x in cm')
    ax1.set_ylabel('Position z in cm')
    
    #cbar = ax1.figure.colorbar(im4, ax=ax4)
    im2 = ax2.imshow(bx_bereinigt, cmap='viridis',vmin=-0.8,vmax=0.8)
    ax2.set_xticks(xstriche)
    ax2.set_xticklabels(xachse)
    ax2.set_yticks(zstriche)
    ax2.set_yticklabels(zachse)
    ax2.set_title('x')
    ax2.xaxis.set_minor_locator(MultipleLocator(1))
    
    
    ax2.set_xlabel('Position x in cm')
    ax2.set_ylabel('Position z in cm')
    
    #cbar = ax2.figure.colorbar(im4, ax=ax4)
    im3 = ax3.imshow(by_bereinigt, cmap='viridis',vmin=-0.8,vmax=0.8)
    ax3.set_xticks(xstriche)
    ax3.set_xticklabels(xachse)
    ax3.set_yticks(zstriche)
    ax3.set_yticklabels(zachse)
    ax3.set_title('y')
    ax3.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax3.set_xlabel('Position x in cm')
    ax3.set_ylabel('Position z in cm')
    
    #cbar = ax3.figure.colorbar(im4, ax=ax4)
    im4 = ax4.imshow(bz_bereinigt, cmap='viridis',vmin=-0.8,vmax=0.8)
    ax4.set_xticks(xstriche)
    ax4.set_xticklabels(xachse)
    ax4.set_yticks(zstriche)
    ax4.set_yticklabels(zachse)
    ax4.set_title('z')
    ax4.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax4.set_xlabel('Position x in cm')
    ax4.set_ylabel('Position z in cm')
    cbar = ax4.figure.colorbar(im4, ax=[ax1,ax2,ax3,ax4], orientation='vertical', fraction=0.047, pad=0.1 ,shrink=0.85)
    cbar.set_label('Magnetic field B in mT')
    fig.suptitle('Edge magnetic field in front of the magnet in the x-z-plane at height y={} cm'.format(hoehe[n]))
    plt.savefig('Randfelder/randfeld_ebene_{}.pdf'.format(name[n]),bbox_inches='tight')
    plt.show()

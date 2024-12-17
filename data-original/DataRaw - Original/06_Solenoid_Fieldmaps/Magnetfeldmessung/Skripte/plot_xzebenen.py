# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:32:05 2023
Auswertung Solenoidmagnetfeld - Ebenenweise

Format Dateien: 6 Infozeilen oben
Spalte 1-3: x,y,z Koordinate
Spalte 4: Babs
Spalte 5-8: Bx,By,Bz
@author: mseeger
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator,AutoMinorLocator)

#Definitionen die für Dateinamen und Beschriftungen benötigt werden
messungen=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21']
hoehe = np.arange(20,-21,-2)
breite = [7,11,13,15,15,17,17,19,19,19,21,19,19,19,17,17,15,15,13,11,7] #Breiten in Rechnung_Messung.xlsx berechnet


#Nochmal für Untergrundmessung    
messungen_ug=['22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42']

for n in range(21):

    #Definitionen Achsenbeschriftung
    ortminuszehn=[0,0,1,2,2,3,3,4,4,4,0,4,4,4,3,3,2,2,1,0,0]
    zachse = np.arange(-6.5,6.6,1)
    if n in [0,20]:
        xachse = ['-0.6','0','0.6']
        xstriche = np.arange(0,breite[n],3)
    
    elif n == 10:
        xachse = np.arange(-2.0,2.1,1)
        xstriche = np.arange(0,breite[n],5)
        
    else:
        xachse = np.arange(-1.0,1.1,1)
        xstriche = np.arange(ortminuszehn[n],breite[n],5)
        
    plt.rc('xtick', labelsize=8)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=8)    # fontsize of the tick labels
        
        
    #Laden und Anpassen der Daten
    ebene = np.loadtxt('Solenoid_Messung{}_3-5A_h{}.txt'.format(messungen[n],hoehe[n]),skiprows=6)#lade Dateien
    babs = np.reshape(ebene[:,3],(66,breite[n])) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
    babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
    bx = np.reshape(ebene[:,4],(66,breite[n]))
    bx[1::2, :] = bx[1::2, ::-1]
    by = np.reshape(ebene[:,5],(66,breite[n]))
    by[1::2, :] = by[1::2, ::-1]
    bz = np.reshape(ebene[:,6],(66,breite[n]))
    bz[1::2, :] = bz[1::2, ::-1] 
    
    #Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
    bx_real = -1000*by 
    by_real = 1000*bx
    bz_real = -1000*bz
    babs = 1000*babs
    
    #2D-Plot Heatmap
    #4 Plots einer Ebene in einem
    #imshow hat Ursprung in oberer linker Ecke, x-Achse geht nach unten, y-Achse nach rechts!
    fig, (ax1,ax2,ax3,ax4) = plt.subplots(nrows=1,ncols=4,figsize = (10,5))
    im1 = ax1.imshow(babs, cmap='viridis',  vmin=-35 ,vmax=35)
    ax1.set_title('Abs.')
    ax1.set_xticks(xstriche)
    ax1.set_xticklabels(xachse)
    ax1.set_yticks(np.arange(0,66,5))
    ax1.set_yticklabels(zachse)
    ax1.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax1.set_xlabel('Position x in cm')
    ax1.set_ylabel('Position z in cm')
    
    #cbar = ax1.figure.colorbar(im4, ax=ax4)
    im2 = ax2.imshow(bx_real, cmap='viridis',  vmin=-35 ,vmax=35)
    ax2.set_xticks(xstriche)
    ax2.set_xticklabels(xachse)
    ax2.set_yticks(np.arange(0,66,5))
    ax2.set_yticklabels(zachse)
    ax2.set_title('x')
    ax2.xaxis.set_minor_locator(MultipleLocator(1))
    
    
    ax2.set_xlabel('Position x in cm')
    ax2.set_ylabel('Position z in cm')
    
    #cbar = ax2.figure.colorbar(im4, ax=ax4)
    im3 = ax3.imshow(by_real, cmap='viridis',  vmin=-35 ,vmax=35)
    ax3.set_xticks(xstriche)
    ax3.set_xticklabels(xachse)
    ax3.set_yticks(np.arange(0,66,5))
    ax3.set_yticklabels(zachse)
    ax3.set_title('y')
    ax3.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax3.set_xlabel('Position x in cm')
    ax3.set_ylabel('Position z in cm')
    
    #cbar = ax3.figure.colorbar(im4, ax=ax4)
    im4 = ax4.imshow(bz_real, cmap='viridis',  vmin=-35 ,vmax=35)
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
    #fig.suptitle('Magnetic field in the x-z-plane at height y={}'.format(hoehe[n]),fontsize=10)
    plt.tight_layout()
    plt.savefig('xz-Ebenenplots/plot_xz_total_h{}.pdf'.format(hoehe[n]))
    plt.show()
 
    #Nochmal für Untergrundmessung
    #Laden und Anpassen der Daten
    ebene_ug = np.loadtxt('Solenoid_Messung{}_0A_h{}.txt'.format(messungen_ug[n],hoehe[20-n]),skiprows=6)#lade Dateien
    babs_ug = np.reshape(ebene_ug[:,3],(66,breite[n])) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
    babs_ug[1::2, :] = babs_ug[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde
    bx_ug = np.reshape(ebene_ug[:,4],(66,breite[n]))
    bx_ug[1::2, :] = bx_ug[1::2, ::-1]
    by_ug = np.reshape(ebene_ug[:,5],(66,breite[n]))
    by_ug[1::2, :] = by_ug[1::2, ::-1]
    bz_ug = np.reshape(ebene_ug[:,6],(66,breite[n]))
    bz_ug[1::2, :] = bz_ug[1::2, ::-1] 
    
    #Transformation Magnetfeldrichtung Sonde in Strahlkoordinatensystem
    bx_real_ug = -1000*by_ug 
    by_real_ug = 1000*bx_ug
    bz_real_ug = -1000*bz_ug
    babs_ug = 1000*babs_ug
    
    #2D-Plot Heatmap
    #4 Plots einer Ebene in einem
    #imshow hat Ursprung in oberer linker Ecke, x-Achse geht nach unten, y-Achse nach rechts!
    fig, (ax1,ax2,ax3,ax4) = plt.subplots(nrows=1,ncols=4,figsize = (10,5))
    im1 = ax1.imshow(babs_ug, cmap='viridis',vmin=-0.13,vmax=0.13)
    ax1.set_title('Abs.')
    ax1.set_xticks(xstriche)
    ax1.set_xticklabels(xachse)
    ax1.set_yticks(np.arange(0,66,5))
    ax1.set_yticklabels(zachse)
    ax1.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax1.set_xlabel('Position x in cm')
    ax1.set_ylabel('Position z in cm')
    
    #cbar = ax1.figure.colorbar(im4, ax=ax4)
    im2 = ax2.imshow(bx_real_ug, cmap='viridis',vmin=-0.13,vmax=0.13)
    ax2.set_xticks(xstriche)
    ax2.set_xticklabels(xachse)
    ax2.set_yticks(np.arange(0,66,5))
    ax2.set_yticklabels(zachse)
    ax2.set_title('x')
    ax2.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax2.set_xlabel('Position x in cm')
    ax2.set_ylabel('Position z in cm')
    
    #cbar = ax2.figure.colorbar(im4, ax=ax4)
    im3 = ax3.imshow(by_real_ug, cmap='viridis',vmin=-0.13,vmax=0.13)
    ax3.set_xticks(xstriche)
    ax3.set_xticklabels(xachse)
    ax3.set_yticks(np.arange(0,66,5))
    ax3.set_yticklabels(zachse)
    ax3.set_title('y')
    ax3.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax3.set_xlabel('Position x in cm')
    ax3.set_ylabel('Position z in cm')
    
    #cbar = ax3.figure.colorbar(im4, ax=ax4)
    im4 = ax4.imshow(bz_real_ug, cmap='viridis',vmin=-0.13,vmax=0.13)
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
    #fig.suptitle('Background magnetic field in the x-z-plane at height y={}'.format(hoehe[n]),fontsize=10)
    plt.tight_layout()
    plt.savefig('xz-Ebenenplots/plot_xz_untergrund_h{}.pdf'.format(hoehe[n]))
    plt.show()
    
    #Messung-Untergrund
    babs_bereinigt = babs - babs_ug
    bx_bereinigt = bx_real - bx_real_ug
    by_bereinigt = by_real - by_real_ug
    bz_bereinigt = bz_real - bz_real_ug
    
    #2D-Plot Heatmap
    #4 Plots einer Ebene in einem
    #imshow hat Ursprung in oberer linker Ecke, x-Achse geht nach unten, y-Achse nach rechts!
    fig, (ax1,ax2,ax3,ax4) = plt.subplots(nrows=1,ncols=4,figsize = (10,5))
    im1 = ax1.imshow(babs_bereinigt, cmap='viridis', vmin=-35 ,vmax=35)
    ax1.set_title('Abs.')
    ax1.set_xticks(xstriche)
    ax1.set_xticklabels(xachse)
    ax1.set_yticks(np.arange(0,66,5))
    ax1.set_yticklabels(zachse)
    ax1.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax1.set_xlabel('Position x in cm')
    ax1.set_ylabel('Position z in cm')
    #cbar = ax1.figure.colorbar(im4, ax=ax4)
    im2 = ax2.imshow(bx_bereinigt, cmap='viridis', vmin=-35 ,vmax=35)
    ax2.set_xticks(xstriche)
    ax2.set_xticklabels(xachse)
    ax2.set_yticks(np.arange(0,66,5))
    ax2.set_yticklabels(zachse)
    ax2.set_title('x')
    ax2.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax2.set_xlabel('Position x in cm')
    ax2.set_ylabel('Position z in cm')
    #cbar = ax2.figure.colorbar(im4, ax=ax4)
    im3 = ax3.imshow(by_bereinigt, cmap='viridis', vmin=-35 ,vmax=35)
    ax3.set_xticks(xstriche)
    ax3.set_xticklabels(xachse)
    ax3.set_yticks(np.arange(0,66,5))
    ax3.set_yticklabels(zachse)
    ax3.set_title('y')
    ax3.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax3.set_xlabel('Position x in cm')
    ax3.set_ylabel('Position z in cm')
    #cbar = ax3.figure.colorbar(im4, ax=ax4)
    im4 = ax4.imshow(bz_bereinigt, cmap='viridis', vmin=-35 ,vmax=35)
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
    #fig.suptitle('Magnetic field in the x-z-plane at height y={}, background subtracted'.format(hoehe[n]),fontsize=10)
    plt.tight_layout()
    plt.savefig('xz-Ebenenplots/plot_xz_bereinigt_h{}.pdf'.format(hoehe[n]))
    plt.show()
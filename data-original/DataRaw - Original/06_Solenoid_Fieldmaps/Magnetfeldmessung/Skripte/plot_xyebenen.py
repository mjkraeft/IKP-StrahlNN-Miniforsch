# -*- coding: utf-8 -*-
"""
Created on Mon May 22 09:44:47 2023

@author: Merle
"""


import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

'''
ebene = np.loadtxt('Solenoid_Messung11_3-5A_h0.txt',skiprows=6)
babs = np.reshape(ebene[:,3],(66,21))
babs[1::2, :] = babs[1::2, ::-1] 
bx = np.reshape(ebene[:,4],(66,21))
bx[1::2, :] = bx[1::2, ::-1] 
by = np.reshape(ebene[:,5],(66,21))
by[1::2, :] = by[1::2, ::-1] 
bz = np.reshape(ebene[:,6],(66,21))
bz[1::2, :] = bz[1::2, ::-1] 

bx_real = -by #Umbauen in Strahlkoordinatensystem/Plotsystem
by_real = bx #kein Minus! Minus von z-Richtungsumrechnung mal Minus von Magnetfeldumrechnung gibt plus!
bz_real = -bz

b_transversal = np.sqrt(bx_real**2+by_real**2)
fig, ax = plt.subplots(figsize = (5,5))
im = ax.imshow(b_transversal, cmap='viridis')
#plt.savefig('test.pdf')
plt.show()

for n in range(66):
    mini = np.argmin(b_transversal[n,:])
    print(n , mini)
'''
    
messungen=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22']
hoehe = np.arange(20,-21,-2)
breite = [7,11,13,15,15,17,17,19,19,19,21,19,19,19,17,17,15,15,13,11,7]

Bx_3d = np.full((66,21,21),np.nan)
By_3d = np.full((66,21,21),np.nan)
Bt_3d = np.full((66,21,21),np.nan)

Bx_3d_a = np.full((66,21,21),np.nan)
By_3d_a = np.full((66,21,21),np.nan)
Bt_3d_a = np.full((66,21,21),np.nan)

for n in range(21):
    data = np.loadtxt('Solenoid_Messung{}_3-5A_h{}.txt'.format(messungen[n],hoehe[n]),skiprows=6)
    xstart = int((21-breite[n])/2) #berechne Bereich
    xend = int(21 - xstart)
    Bx = np.reshape(data[:,4],(66,breite[n]))
    Bx[1::2, :] = Bx[1::2, ::-1] #Umdrehen jeder zweiten Messreihe wg Schlangenform
    By = np.reshape(data[:,5],(66,breite[n]))
    By[1::2, :] = By[1::2, ::-1]  
    bx_real = -By #Umrechnung von Achse der Sonde zu geometrischer Achse 
    by_real = Bx
    
    
    Bx_3d_a[:,xstart:xend,20-n] = 1000*bx_real #20-n weil ich von oben anfange, die Zählung aber unten, Umrechnen in milliTesla
    By_3d_a[:,xstart:xend,20-n] = 1000*by_real
    Bt_3d_a[:,xstart:xend,20-n] = 1000*np.sqrt(bx_real**2+by_real**2) #absoluter Wert des transversalen Magnetfelds
    
    Bx_3d[:,xstart:xend,n] = 1000*bx_real #von unten anfangen für imshow (xachse von oben nach unten, umgekehrt wie erwartet), Umrechnen in milliTesla
    By_3d[:,xstart:xend,n] = 1000*by_real
    Bt_3d[:,xstart:xend,n] = 1000*np.sqrt(bx_real**2+by_real**2) #absoluter Wert des transversalen Magnetfelds
    
print(np.nanmin(Bt_3d),np.nanmax(Bt_3d))
 
#suche Minima, x-y-ebenenweise
write = np.zeros((66,4)) #Array, um Ergebnisse zu speichern
location = np.zeros((66,3)) #Array für den 3D scatter plot
for m in range(66):
    #berechne z-koordinate
    #zkoord = 0.2*m-6.5
    location[m,2]=m #Struktur location array: x y z
    
    #Suche Minimum und dessen Ort:
    #print(m, np.nanargmin(Bt_3d[m,:,:]),np.nanmin(Bt_3d[m,:,:])) 
    write[m,0]=m
    write[m,1]=np.nanargmin(Bt_3d[m,:,:])
    write[m,2]=np.nanmin(Bt_3d[m,:,:])
    write[m,3]=np.nanmean(Bt_3d[m,:,:])
    
    #Berechnen der x- und y- Koordinaten des Minimums
    xkoord = np.floor((write[m,1]/21))
    location[m,0]=xkoord
    ykoord = write[m,1]-((xkoord)*21)
    location[m,1]=ykoord
    
    
print(location)    

#3D Scatter Plot

plt.figure(figsize=(6,2))
plt.plot(location[:,2],location[:,0],'s',marker='.',label='x-direction',color='lightseagreen',ms=2)
plt.plot(location[:,2],location[:,1],'s',marker='.',label='y-direction',color='cornflowerblue',ms=2)
plt.title('Magnetic axis - location of the minimum abs. values of the transverse field')
plt.legend()
plt.xticks(np.arange(0,66,5),np.arange(-6.5,6.6,1))
plt.xlabel('Position z in cm')
plt.ylim(ymin=0,ymax=20)
plt.yticks(np.arange(0,21,5),np.arange(-2.0,2.1,1))
plt.ylabel('Position in cm')
#plt.savefig('minima_ort.pdf',bbox_inches='tight')
plt.show()

plt.figure(figsize=(6,4))
plt.bar(write[:,0],write[:,3],color='yellowgreen',label = 'mean')
plt.bar(write[:,0],write[:,2],color='cornflowerblue', label = 'minimum')
plt.title('Minimum abs. values and mean abs. values of the transverse field')
plt.legend()
plt.xticks(np.arange(0,66,5),np.arange(-6.5,6.6,1))
plt.xlabel('Position z in cm')
plt.ylabel('Abs. magnetic field in mT')
plt.savefig('minimaandmean.pdf',bbox_inches='tight')
plt.show()

plt.bar(write[:,0],write[:,3])
plt.show()
    
#beide in einem:


fig, (ax1,ax2) = plt.subplots(nrows=2,ncols=1,figsize = (6,4))
ax1.plot(location[:,2],location[:,0],'s',marker='+',label='x-direction',color='lightseagreen',ms=3)
ax1.plot(location[:,2],location[:,1],'s',marker='x',label='y-direction',color='cornflowerblue',ms=3)
fig.suptitle('Magnetic axis - Minimum abs. values of the transverse field')
ax1.legend()
ax1.set_xticks(np.arange(0,66,5))
ax1.set_xticklabels(np.arange(-6.5,6.6,1))
ax1.set_xlabel('Position z in cm')
ax1.set_ylim(ymin=0,ymax=20)
ax1.set_yticks(np.arange(0,21,5))
ax1.set_yticklabels(np.arange(-2.0,2.1,1))
ax1.set_ylabel('Position in cm')

plt.bar(write[:,0],write[:,3])
ax2.bar(write[:,0],write[:,2],color='yellowgreen')
ax2.set_xticks(np.arange(0,66,5))
ax2.set_xticklabels(np.arange(-6.5,6.6,1))
ax2.set_xlabel('Position z in cm')
ax2.set_ylabel('Abs. magnetic field in mT')
#plt.savefig('minima_mitfeld.pdf',bbox_inches='tight')
plt.show()

 
np.savetxt('magnetachse.txt',write)

'''
for m in range(66):
    #berechne z-koordinaten
    zkoord = 0.2*m-6.5
    xt = np.arange(0,21,5)
    xtlabel = np.arange(-2,2.1,1)
    yt = np.arange(0,21,5)
    ytlabel = np.arange(2.0,-2.1,-1)
    
    #Schriftgroessen
    plt.rc('axes', titlesize=10)     # fontsize of the axes title
    plt.rc('axes', labelsize=10)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=8)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=8)    # fontsize of the tick labels
    
    
    #fig, (ax1,ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (6,2))
    fig, ax1 = plt.subplots(figsize=(4,3))
    im1 = ax1.pcolormesh(Bt_3d[m,:,:].transpose(), cmap='viridis', edgecolors='none')
    ax1.set_title('Cutting plane {}:   z={}cm'.format(m,np.round(zkoord,1)))
    ax1.set_xticks(xt)
    ax1.set_xticklabels(xtlabel)
    ax1.set_yticks(xt)
    ax1.set_yticklabels(xtlabel)
    ax1.set_xlabel('Position x in cm')
    ax1.set_ylabel('Position y in cm')
    fig.colorbar(im1,ax = ax1, label = 'Transv. magn. field in mT')
    ax1.set_aspect('equal', adjustable='box')
    plt.savefig('xy-Ebenenplots/plot_cmap_xyebene{}.pdf'.format(m),bbox_inches='tight')
    
    
    fig, ax1 = plt.subplots(figsize=(4,3))
    im1 = ax1.imshow(Bt_3d[m,:,:].transpose(), cmap='viridis')
    ax1.set_title('Cutting plane {}:   z={}cm'.format(m,np.round(zkoord,1)))
    ax1.set_xticks(xt)
    ax1.set_xticklabels(xtlabel)
    ax1.set_yticks(yt)
    ax1.set_yticklabels(ytlabel)
    ax1.set_xlabel('Position x in cm')
    ax1.set_ylabel('Position y in cm')
    fig.colorbar(im1,ax = ax1, label = 'Transv. magn. field in mT')
    ax1.set_aspect('equal', adjustable='box')
    plt.savefig('xy-Ebenenplots/plot_cmap_xyebene{}.pdf'.format(m),bbox_inches='tight')
    
    
    fig, ax2 = plt.subplots(figsize=(4,3))
    ax2 = plt.gca()
    ax2.set_title('Cutting plane {}:   z={}cm'.format(m,np.round(zkoord,1)))
    B = ax2.quiver(Bx_3d_a[m,:,:].transpose(), By_3d_a[m,:,:].transpose(), Bt_3d_a[m,:,:].transpose(), cmap = 'viridis')
    ax2.set_xticks(xt)
    ax2.set_xticklabels(xtlabel)
    ax2.set_yticks(xt)
    ax2.set_yticklabels(xtlabel)
    ax2.set_xlabel('Position x in cm',fontsize=10)
    ax2.set_ylabel('Position y in cm')
    ax2.set_aspect('equal', adjustable='box')
    fig.colorbar(B,label = 'Transv. magn. field in mT')
    plt.savefig('xy-Ebenenplots/plot_arrows_xyebene{}.pdf'.format(m),bbox_inches='tight')
    plt.draw()
    plt.show()

'''

    


    

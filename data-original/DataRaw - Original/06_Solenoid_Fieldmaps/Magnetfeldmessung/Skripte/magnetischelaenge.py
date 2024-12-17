# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 16:25:01 2023

@author: ms
"""

import numpy as np
import matplotlib.pyplot as plt

ebene = np.loadtxt('Solenoid_Messung11_3-5A_h0.txt',skiprows=6)
simulation = np.loadtxt('simulation/ende_zachse.txt', skiprows=2)

babs = np.reshape(ebene[:,3],(66,21)) #Umformung Liste zu 2D Matrix der Magnetfeldwerte (Position in Matrix kodiert Ort)
babs[1::2, :] = babs[1::2, ::-1] #Umdrehen jeder zweiten Reihe wg schlangenförmigem Fahrmuster der Sonde

magnetfeld = np.multiply(babs[:,10],1000) #auswählen und umrechnen in MilliTesla
simulation[:,1] = np.multiply(simulation[:,1],1000) #umrechnen in MilliTesla

zachse = np.arange(-6.5,6.6,0.2)
zsimulation = np.multiply(simulation[:,0],0.1)

fig = plt.figure(figsize=(5,3.75))
plt.plot(zachse, magnetfeld, marker = 'x', color = 'yellowgreen',label='Measurement')
plt.plot(zsimulation,simulation[:,1], color = 'lightseagreen',label = 'Simulation')
plt.legend()
plt.xlabel('Position z in cm')
plt.ylabel('Magnetic field in mT')
plt.savefig('magnetischelaenge.pdf',bbox_inches = 'tight')
plt.show()

integral = np.trapz(magnetfeld,zachse)
print(integral)
bmax = np.amax(magnetfeld)
print(bmax)

length = integral/bmax
print(length)

def f(B,l):
    k = ((1.6022e-19*3e8)/(2*1.489*0.741*9.11e-31*(3e8)**2))**2
    return 1/(k*(B*1e-3)**2*(l*0.1))

print(f(bmax,length))
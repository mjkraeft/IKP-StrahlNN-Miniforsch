import os

os.system("elegant simulation_slave.ele > simulation_slave.log")
os.system("sddsprintout simulation_slave.fin -parameter=Cx -parameter=Cy -parameter=Sx -parameter=Sy -parameter=Particles -width=200 >> output.txt")